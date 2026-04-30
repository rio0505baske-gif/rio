from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

doc = Document()

# ページ設定（A4）
section = doc.sections[0]
section.page_height = Cm(29.7)
section.page_width = Cm(21.0)
section.top_margin = Cm(1.5)
section.bottom_margin = Cm(1.5)
section.left_margin = Cm(1.8)
section.right_margin = Cm(1.8)

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def add_heading(doc, text, level=1, color='1F3864'):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(11 if level == 1 else 9.5)
    run.font.color.rgb = RGBColor.from_string(color)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    return p

# ========== タイトル ==========
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_run = title_p.add_run('事前調査シート　／　先斗町エリア 居酒屋')
title_run.bold = True
title_run.font.size = Pt(14)
title_run.font.color.rgb = RGBColor.from_string('FFFFFF')

# タイトル背景色
from docx.oxml import OxmlElement
pPr = title_p._p.get_or_add_pPr()
shd = OxmlElement('w:shd')
shd.set(qn('w:val'), 'clear')
shd.set(qn('w:color'), 'auto')
shd.set(qn('w:fill'), '1F3864')
pPr.append(shd)
title_p.paragraph_format.space_before = Pt(4)
title_p.paragraph_format.space_after = Pt(4)

# 日付・作成者
meta_p = doc.add_paragraph()
meta_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
meta_run = meta_p.add_run(f'作成日：{datetime.date.today().strftime("%Y年%m月%d日")}　　担当ブランド：AIでええやんハイボール　　会社：AIでええやん飲料株式会社')
meta_run.font.size = Pt(8)
meta_run.font.color.rgb = RGBColor.from_string('666666')
meta_p.paragraph_format.space_after = Pt(4)

# ========== 1. エリア概要 ==========
add_heading(doc, '■ 1. エリア概要')
area_table = doc.add_table(rows=1, cols=2)
area_table.style = 'Table Grid'
area_table.alignment = WD_TABLE_ALIGNMENT.LEFT

row = area_table.rows[0]
row.cells[0].width = Cm(3.5)
row.cells[1].width = Cm(14.5)

set_cell_bg(row.cells[0], 'D6E4F0')
row.cells[0].paragraphs[0].add_run('エリア概要').bold = True
row.cells[0].paragraphs[0].runs[0].font.size = Pt(9)
c1 = row.cells[1]
c1_p = c1.paragraphs[0]
c1_p.add_run(
    '京都市中京区先斗町 ／ 鴨川と木屋町通の間、約500mの石畳の細路地\n'
    '先斗町のれん会加盟店：74店舗（三条〜四条間）\n'
    '客層：外国人観光客（インバウンド急増）・国内観光客・地元若者・宴会ビジネス層\n'
    '繁忙帯：18時以降〜深夜　夏季（5〜9月）は鴨川納涼床で集客大幅増'
).font.size = Pt(8.5)

doc.add_paragraph()

# ========== 2. 代表店舗 ==========
add_heading(doc, '■ 2. 代表店舗リスト（ターゲット候補）')

shops_table = doc.add_table(rows=6, cols=4)
shops_table.style = 'Table Grid'
headers = ['店名', 'ジャンル／席数', '夜の価格帯', 'ハイボール状況・営業メモ']
widths = [Cm(4.0), Cm(3.5), Cm(2.5), Cm(8.0)]

for i, (h, w) in enumerate(zip(headers, widths)):
    cell = shops_table.rows[0].cells[i]
    cell.width = w
    set_cell_bg(cell, '1F3864')
    p = cell.paragraphs[0]
    run = p.add_run(h)
    run.bold = True
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor.from_string('FFFFFF')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

data = [
    ('先斗町酒場\n（串カツ・大衆）', '串カツ居酒屋\n〜40名', '¥2,000〜2,999', '★優先★ セルフサーバータワー導入済。飲み放題重視。ハイボール消費量大。仕入れコスト感度高い。'),
    ('もつ鍋 寅屋', 'もつ鍋・居酒屋\n20〜30名', '¥3,000〜4,000', 'ビール・サワー中心。ハイボールへのシフト提案余地あり。もつ鍋との相性訴求可能。'),
    ('先斗町 ますだ', 'おばんざい・京料理\n個室あり 20〜30名', '¥3,000〜5,000', '観光客・地元客両方に人気。ドリンクラインナップ充実への関心あり。品質提案向き。'),
    ('ハイボールBAR\n京都1923', 'ハイボール専門\n小規模', '¥3,000〜4,000', 'ハイボール飲み放題コースあり。業務用ウイスキーの品質・コスト改善提案余地あり。'),
    ('魯ビン（ろびん）', '京会席・鴨川床\n〜30名', '¥5,000〜8,000', '高単価。インバウンド向け「日本ウイスキー体験」演出との親和性高い。'),
]

for i, (a, b, c, d) in enumerate(data):
    row = shops_table.rows[i + 1]
    bg = 'EBF5FB' if i % 2 == 0 else 'FDFEFE'
    for j, (cell, txt) in enumerate(zip(row.cells, [a, b, c, d])):
        set_cell_bg(cell, bg)
        p = cell.paragraphs[0]
        run = p.add_run(txt)
        run.font.size = Pt(8)

doc.add_paragraph()

# ========== 3. ドリンク市場 ==========
add_heading(doc, '■ 3. ドリンク市場・競合状況')

drink_table = doc.add_table(rows=1, cols=3)
drink_table.style = 'Table Grid'

hdrs = ['ハイボール相場', '原価構造（業界標準）', 'トレンド・インサイト']
widths2 = [Cm(5.5), Cm(5.5), Cm(7.0)]
for i, (h, w) in enumerate(zip(hdrs, widths2)):
    c = drink_table.rows[0].cells[i]
    c.width = w
    set_cell_bg(c, 'D6E4F0')
    p = c.paragraphs[0]
    run = p.add_run(h)
    run.bold = True
    run.font.size = Pt(8.5)

row2 = drink_table.add_row()
txts = [
    '単品：350〜550円\n飲み放題込み：60分600円〜\n2時間コース：2,500円前後\nプレミアム：3,500円〜',
    '業務用ウイスキー4L：3,000〜5,000円\n1杯原価（ウイスキー30ml）：50〜60円\n原価率：10〜15%（業界最高利益率）',
    '・セルフサーバーがSNS映え→口コミ拡散\n・インバウンド需要で「日本ウイスキー体験」注目\n・クラフト・国産ウイスキー人気上昇中\n・観光地価格が通りやすいエリア特性'
]
for i, txt in enumerate(txts):
    p = row2.cells[i].paragraphs[0]
    run = p.add_run(txt)
    run.font.size = Pt(8)

doc.add_paragraph()

# ========== 4. 提案角度3つ ==========
add_heading(doc, '■ 4. 提案角度（3パターン）')

angles = [
    ('角度①', '原価率改善×飲み放題強化', '1F3864',
     '課題：飲み放題コースのドリンク原価が高く、利益が圧迫されている\n'
     '提案：ビール（原価率45%）→ AIでええやんハイボール（32%）へシフトで▲13pt改善\n'
     '数字：ハイボール200杯/月増加で原価差額 約13,000円/月の利益改善\n'
     'トーク：「飲み放題にハイボールを加えるだけで、コストを抑えながら客満足度が上がります」'),
    ('角度②', 'インバウンド差別化×サーバー体験演出', '1D6A39',
     '課題：外国人観光客が増えているが、他店との差別化ポイントが弱い\n'
     '提案：サーバー無償貸与＋「日本ウイスキー文化体験」演出でSNS映えコンテンツ化\n'
     '数字：サーバー導入0円・POP・メニュー表デザインも無償提供\n'
     'トーク：「訪日外国人が"日本らしい体験"として写真を撮ってSNSに拡散してくれます」'),
    ('角度③', 'リスクゼロ試験導入×客単価+380円実証', '7D3C00',
     '課題：新しい商品の導入に踏み切れない（初期コスト・在庫リスク懸念）\n'
     '提案：サーバー無償貸与＋1ヶ月お試しで初期投資ゼロ。効果確認後に継続判断\n'
     '数字：導入店舗の客単価平均+380円 ／ 30席×1.5回転×25日 = 月+427,500円試算\n'
     'トーク：「費用ゼロで始めて、1ヶ月で効果が出なければやめていただいて構いません」'),
]

for label, title, color, body in angles:
    p = doc.add_paragraph()
    run_label = p.add_run(f'【{label}】')
    run_label.bold = True
    run_label.font.size = Pt(9)
    run_label.font.color.rgb = RGBColor.from_string(color)
    run_title = p.add_run(f' {title}')
    run_title.bold = True
    run_title.font.size = Pt(9)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1)

    body_p = doc.add_paragraph()
    body_run = body_p.add_run(body)
    body_run.font.size = Pt(8.5)
    body_p.paragraph_format.left_indent = Cm(0.5)
    body_p.paragraph_format.space_after = Pt(4)

# ========== 5. 次のアクション ==========
add_heading(doc, '■ 5. 次のアクション')
actions_table = doc.add_table(rows=1, cols=3)
actions_table.style = 'Table Grid'

for i, (h, w) in enumerate(zip(['優先アプローチ店', '初回トーク切り口', '持参ツール'], [Cm(5.5), Cm(6.0), Cm(6.5)])):
    c = actions_table.rows[0].cells[i]
    c.width = w
    set_cell_bg(c, '1F3864')
    run = c.paragraphs[0].add_run(h)
    run.bold = True
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor.from_string('FFFFFF')
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

row3 = actions_table.add_row()
row3_txts = [
    '① 先斗町酒場（飲み放題重視）\n② もつ鍋 寅屋（ビール中心からの転換）\n③ ハイボールBAR京都1923（品質向上提案）',
    '「今、ドリンクの利益率で気になっていることはありますか？」\n→ 課題を先に聞いてから提案角度を選択',
    '・原価率比較資料\n・客単価+380円実績シート\n・サーバー仕様書\n・POP・メニューサンプル'
]
for i, txt in enumerate(row3_txts):
    p = row3.cells[i].paragraphs[0]
    run = p.add_run(txt)
    run.font.size = Pt(8)

# フッター
footer_p = doc.add_paragraph()
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer_run = footer_p.add_run('── AIでええやん飲料株式会社　営業部 ──')
footer_run.font.size = Pt(7.5)
footer_run.font.color.rgb = RGBColor.from_string('999999')
footer_p.paragraph_format.space_before = Pt(8)

# 保存
output_path = '/home/user/rio/highball-sales/output/調査シート/先斗町_居酒屋_事前調査シート.docx'
doc.save(output_path)
print(f'Saved: {output_path}')
