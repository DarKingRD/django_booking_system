// frontend/script.js
// Настройки
const API_URL = 'http://localhost:8000/api';

// Глобальные переменные
let tokens = null;
let userId = null;

// DOM-элементы, которые не зависят от контента
const userInfo = document.getElementById('user-info');
const authBtn = document.getElementById('auth-btn');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

// === При загрузке страницы ===
document.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('auth');
  if (saved) {
    const data = JSON.parse(saved);
    tokens = data.tokens;
    userId = data.userId;
    updateAuthUI();
    loadBookings();
  }
  loadRooms(); // Загружаем комнаты всегда
});

// === Обновление интерфейса авторизации ===
function updateAuthUI() {
  if (tokens) {
    userInfo.textContent = `Пользователь: ${userId}`;
    authBtn.textContent = 'Выйти';
    authBtn.onclick = logout;
  } else {
    userInfo.textContent = 'Гость';
    authBtn.textContent = 'Войти';
    authBtn.onclick = () => {
      const tab = new bootstrap.Tab(document.querySelector('[href="#auth"]'));
      tab.show();
    };
  }
}

// === Вход ===
loginForm.onsubmit = async (e) => {
  e.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  try {
    const res = await fetch(`${API_URL}/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      alert('Ошибка входа: ' + JSON.stringify(err, null, 2));
      return;
    }

    const data = await res.json();
    tokens = data;
    userId = username;

    localStorage.setItem('auth', JSON.stringify({ tokens, userId }));

    alert('Вход успешен!');
    updateAuthUI();
    loadBookings();
    loadRooms();
  } catch (err) {
    console.error('Ошибка сети:', err);
    alert('Ошибка подключения к серверу');
  }
};

// === Регистрация ===
registerForm.onsubmit = async (e) => {
  e.preventDefault();
  const username = document.getElementById('reg-username').value;
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;

  try {
    const res = await fetch(`${API_URL}/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      alert('Ошибка: ' + JSON.stringify(err, null, 2));
      return;
    }

    alert('Регистрация успешна! Теперь войдите.');
    // Переключаем на вкладку входа
    const tab = new bootstrap.Tab(document.querySelector('[href="#auth"]'));
    tab.show();
  } catch (err) {
    console.error('Ошибка сети:', err);
    alert('Ошибка подключения к серверу');
  }
};

// === Выход ===
function logout() {
  tokens = null;
  userId = null;
  localStorage.removeItem('auth');
  updateAuthUI();
  document.getElementById('bookings-list').innerHTML = '';
  alert('Вы вышли из системы');
}

// === Загрузка комнат ===
async function loadRooms() {
  try {
    const res = await fetch(`${API_URL}/rooms/`);
    console.log('Статус /rooms/:', res.status);

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      console.error('Ошибка API /rooms/:', err);
      return;
    }

    const rooms = await res.json();
    console.log('Комнаты:', rooms);

    const roomsList = document.getElementById('rooms-list');
    roomsList.innerHTML = '';

    if (!Array.isArray(rooms) || rooms.length === 0) {
      roomsList.innerHTML = '<div class="col-12"><p class="text-muted">Нет доступных комнат</p></div>';
      return;
    }

    rooms.forEach(room => {
      const col = document.createElement('div');
      col.className = 'col-md-4 mb-3';
      col.innerHTML = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">🚪 ${room.name}</h5>
            <p class="card-text">
              Вместимость: ${room.capacity} чел.<br>
              ${room.description || 'Без описания'}
            </p>
            <button class="btn btn-sm btn-outline-primary" onclick="bookRoom(${room.id})">
              Забронировать
            </button>
          </div>
        </div>
      `;
      roomsList.appendChild(col);
    });
  } catch (err) {
    console.error('Ошибка загрузки комнат:', err);
    document.getElementById('rooms-list').innerHTML =
      '<div class="col-12"><p class="text-danger">Ошибка загрузки комнат</p></div>';
  }
}

// === Загрузка бронирований ===
async function loadBookings() {
  if (!tokens) return;

  try {
    const res = await fetch(`${API_URL}/bookings/`, {
      headers: {
        'Authorization': `Bearer ${tokens.access}`
      }
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      console.error('Ошибка /bookings/:', err);
      return;
    }

    const bookings = await res.json();
    const bookingsList = document.getElementById('bookings-list');
    bookingsList.innerHTML = '';

    if (!Array.isArray(bookings) || bookings.length === 0) {
      bookingsList.innerHTML = '<li class="list-group-item text-muted">Нет бронирований</li>';
      return;
    }

    bookings.forEach(b => {
      const li = document.createElement('li');
      li.className = 'list-group-item d-flex justify-content-between align-items-center';
      li.innerHTML = `
        <div>
          <strong>${b.room_name || 'Комната'}</strong> — ${b.date}
          <div class="text-muted small">
            ${b.start_time ? new Date(b.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''} —
            ${b.end_time ? new Date(b.end_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
          </div>
        </div>
        <button class="btn btn-sm btn-outline-danger" onclick="cancelBooking(${b.id})">
          Отменить
        </button>
      `;
      bookingsList.appendChild(li);
    });
  } catch (err) {
    console.error('Ошибка загрузки бронирований:', err);
    const bookingsList = document.getElementById('bookings-list');
    bookingsList.innerHTML = '<li class="list-group-item text-danger">Ошибка загрузки</li>';
  }
}

// === Бронирование комнаты ===
async function bookRoom(roomId) {
  if (!tokens) {
    alert('Сначала войдите в систему');
    return;
  }

  const date = prompt('Введите дату (YYYY-MM-DD)', '2025-11-16');
  const start = prompt('Начало (HH:MM)', '10:00');
  const end = prompt('Конец (HH:MM)', '11:00');

  if (!date || !start || !end) return;

  try {
    const res = await fetch(`${API_URL}/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.access}`
      },
      body: JSON.stringify({
        room: roomId,
        date: date,
        start_time: `${date}T${start}:00`,
        end_time: `${date}T${end}:00`
      })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      alert('Ошибка: ' + JSON.stringify(err, null, 2));
      return;
    }

    alert('Комната успешно забронирована!');
    loadBookings();
  } catch (err) {
    console.error('Ошибка сети:', err);
    alert('Ошибка подключения к серверу');
  }
}

// === Отмена бронирования ===
async function cancelBooking(bookingId) {
  if (!tokens) return;

  if (!confirm('Вы уверены, что хотите отменить бронирование?')) return;

  try {
    const res = await fetch(`${API_URL}/bookings/${bookingId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${tokens.access}`
      }
    });

    if (!res.ok) {
      alert('Не удалось отменить бронирование');
      return;
    }

    alert('Бронирование отменено');
    loadBookings();
  } catch (err) {
    console.error('Ошибка отмены:', err);
    alert('Ошибка сети');
  }
}
