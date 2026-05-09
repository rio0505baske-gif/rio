function toggleFaq(btn) {
  const item = btn.closest('.faq__item');
  const answer = item.querySelector('.faq__a');
  const isOpen = btn.classList.contains('open');

  document.querySelectorAll('.faq__q.open').forEach(q => {
    q.classList.remove('open');
    q.closest('.faq__item').querySelector('.faq__a').style.maxHeight = '0';
  });

  if (!isOpen) {
    btn.classList.add('open');
    answer.style.maxHeight = answer.scrollHeight + 'px';
  }
}

function handleSubmit(e) {
  e.preventDefault();
  const form = e.target;
  form.style.display = 'none';
  document.getElementById('success').style.display = 'block';
}

// nav color change on scroll
const nav = document.querySelector('.nav');
window.addEventListener('scroll', () => {
  if (window.scrollY > 80) {
    nav.style.background = 'rgba(15, 26, 19, 0.98)';
  } else {
    nav.style.background = 'rgba(15, 26, 19, 0.95)';
  }
});

// fade-in on scroll
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.problem__card, .solution__item, .result__card, .timeline__item, .pricing__card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});
