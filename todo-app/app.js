const STORAGE_KEY = 'todo-app-items';

let todos = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
let currentFilter = 'all';

const input = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');
const remainingCount = document.getElementById('remaining-count');
const clearCompletedBtn = document.getElementById('clear-completed');
const filterBtns = document.querySelectorAll('.filter-btn');

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

function addTodo() {
  const text = input.value.trim();
  if (!text) return;

  todos.push({ id: Date.now(), text, completed: false });
  input.value = '';
  save();
  render();
}

function toggleTodo(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
    save();
    render();
  }
}

function deleteTodo(id) {
  todos = todos.filter(t => t.id !== id);
  save();
  render();
}

function clearCompleted() {
  todos = todos.filter(t => !t.completed);
  save();
  render();
}

function getFiltered() {
  if (currentFilter === 'active') return todos.filter(t => !t.completed);
  if (currentFilter === 'completed') return todos.filter(t => t.completed);
  return todos;
}

function render() {
  const filtered = getFiltered();

  if (filtered.length === 0) {
    todoList.innerHTML = '<li class="empty-message">タスクがありません</li>';
  } else {
    todoList.innerHTML = filtered.map(todo => `
      <li class="todo-item">
        <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}
          onchange="toggleTodo(${todo.id})">
        <span class="todo-text ${todo.completed ? 'completed' : ''}">${escapeHtml(todo.text)}</span>
        <button class="delete-btn" onclick="deleteTodo(${todo.id})" title="削除">&#x2715;</button>
      </li>
    `).join('');
  }

  const activeCount = todos.filter(t => !t.completed).length;
  remainingCount.textContent = `${activeCount}件残っています`;
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

addBtn.addEventListener('click', addTodo);

input.addEventListener('keydown', e => {
  if (e.key === 'Enter') addTodo();
});

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    currentFilter = btn.dataset.filter;
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    render();
  });
});

clearCompletedBtn.addEventListener('click', clearCompleted);

render();
