import { useState } from 'react'

function App() {
  // Навигация: 'login' | 'boards' | 'tasks'
  const [screen, setScreen] = useState('login')

  // Данные авторизации
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  // Данные досок и задач
  const [boards, setBoards] = useState([])
  const [currentBoard, setCurrentBoard] = useState(null)
  const [tasks, setTasks] = useState([])

  // Состояния для удаления доски
  const [boardToDelete, setBoardToDelete] = useState(null); // Хранит ID доски, которую хотим удалить
  const [showDeleteModal, setShowDeleteModal] = useState(false); // Показывает модалку

  // Формы создания
  const [newBoardTitle, setNewBoardTitle] = useState('')
  const [newTaskTitle, setNewTaskTitle] = useState('')

  // 1. Логин
  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username, password }),
      })
      if (response.ok) {
        setScreen('boards')
        fetchBoards() // Сразу грузим доски
      } else {
        const data = await response.json()
        setError(data.detail || 'Ошибка авторизации')
      }
    } catch (err) {
      setError('Ошибка сети или CORS')
    }
  }

  // 2. Получить все доски пользователя
  const fetchBoards = async () => {
    try {
      const response = await fetch('/api/boards', { credentials: 'include' })
      if (response.ok) {
        const data = await response.json()
        setBoards(data)
      }
    } catch (err) {
      console.error('Не удалось загрузить доски', err)
    }
  }

  // 3. Создать новую доску
  const handleCreateBoard = async (e) => {
    e.preventDefault()
    if (!newBoardTitle.trim()) return
    try {
      const response = await fetch('/api/boards/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name: newBoardTitle }), // Твой бэкенд сам вытащит user_id из куки сессии!
      })
      if (response.ok) {
        setNewBoardTitle('')
        fetchBoards() // Обновляем список досок
      }
    } catch (err) {
      console.error(err)
    }
  }

  // 4. Удалить доску
  const handleDeleteBoard = async () => {
    if (!boardToDelete) return;
    try {
      const response = await fetch(`/api/boards/${boardToDelete}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (response.ok) {
        // Убираем удаленную доску из стейта, чтобы интерфейс обновился моментально
        setBoards(boards.filter(board => board.id !== boardToDelete));
        // Закрываем модалку и сбрасываем ID
        setShowDeleteModal(false);
        setBoardToDelete(null);
      } else {
        const data = await response.json();
        alert(data.detail || 'Не удалось удалить доску');
      }
    } catch (err) {
      console.error('Ошибка при удалении доски:', err);
      alert('Ошибка сети при удалении');
    }
  };

  // 5. Получить задачи конкретной доски
  const fetchTasks = async (boardId) => {
    try {
      const response = await fetch(`/api/boards/${boardId}/tasks`, { credentials: 'include' })
      if (response.ok) {
        const data = await response.json()
        setTasks(data)
      }
    } catch (err) {
      console.error('Не удалось загрузить задачи', err)
    }
  }

  // Клик по доске — проваливаемся внутрь
  const handleSelectBoard = (board) => {
    setCurrentBoard(board)
    setScreen('tasks')
    fetchTasks(board.id)
  }

  // 6. Создать задачу внутри доски
  const handleCreateTask = async (e) => {
    e.preventDefault()
    if (!newTaskTitle.trim()) return
    try {

        if (!currentBoard || !currentBoard.id) {
            console.error("Доска не выбрана");
            return;
        }
      const response = await fetch(`/api/boards/${currentBoard.id}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ title: newTaskTitle, board_id: currentBoard.id }),
      })
      if (response.ok) {
        setNewTaskTitle('')
        fetchTasks(currentBoard.id) // Обновляем задачи
      }
    } catch (err) {
      console.error(err)
    }
  }

  // --- РЕНДЕР ЭКРАНОВ ---

  // ЭКРАН 1: Логин
  if (screen === 'login') {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h2 style={styles.title}>Вход в TaskManager</h2>
          {error && <div style={styles.errorAlert}>{error}</div>}
          <form onSubmit={handleLogin} style={styles.form}>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Логин</label>
              <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} style={styles.input} required />
            </div>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Пароль</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={styles.input} required />
            </div>
            <button type="submit" style={styles.button}>Войти</button>
          </form>
        </div>
      </div>
    )
  }

  // ЭКРАН 2: Выбор Доски
  if (screen === 'boards') {
    return (
      <div style={styles.dashboardContainer}>
        <h2 style={styles.dashboardTitle}>Мои Доски Задач</h2>

        {/* Форма создания доски */}
        <form onSubmit={handleCreateBoard} style={styles.createForm}>
          <input
            type="text"
            placeholder="Название новой доски..."
            value={newBoardTitle}
            onChange={(e) => setNewBoardTitle(e.target.value)}
            style={styles.input}
          />
          <button type="submit" style={styles.createButton}>Создать доску</button>
        </form>

        {/* Сетка досок */}
        <div style={styles.grid}>
          {boards.map(board => (
            <div
              key={board.id}
              onClick={() => handleSelectBoard(board)}
              style={{ ...styles.boardCard, position: 'relative' }} // relative для позиционирования мусорки
            >
              <h3>{board.name}</h3>
              <p style={{fontSize: '12px', color: '#718096'}}>ID Доски: {board.id}</p>

              {/* Иконка мусорки (с e.stopPropagation!) */}
              <button
                onClick={(e) => {
                  e.stopPropagation(); // ОСТАНАВЛИВАЕМ КЛИК ПО КАРТОЧКЕ
                  setBoardToDelete(board.id);
                  setShowDeleteModal(true);
                }}
                style={styles.deleteButton}
                title="Удалить доску"
              >
                🗑️
              </button>
            </div>
          ))}
          {boards.length === 0 && <p style={{color: '#718096'}}>У вас пока нет досок задач.</p>}
        </div>

        {/* Модалка подтверждения удаления */}
        {showDeleteModal && (
          <div style={styles.modalOverlay}>
            <div style={styles.modalContent}>
              <h3>Удалить доску?</h3>
              <p style={{ color: '#e53e3e', fontSize: '14px' }}>Все задачи на этой доске будут удалены навсегда!</p>
              <div style={styles.modalActions}>
                <button onClick={handleDeleteBoard} style={styles.confirmBtn}>Да, удалить</button>
                <button onClick={() => { setShowDeleteModal(false); setBoardToDelete(null); }} style={styles.cancelBtn}>Отмена</button>
              </div>
            </div>
          </div>
        )}

      </div>
    )
  }

  // ЭКРАН 3: Задачи внутри выбранной доски
  if (screen === 'tasks') {
    return (
      <div style={styles.dashboardContainer}>
        <button onClick={() => setScreen('boards')} style={styles.backButton}>← Назад к доскам</button>
        <h2 style={styles.dashboardTitle}>Доска: {currentBoard?.name}</h2>

        {/* Форма создания задачи */}
        <form onSubmit={handleCreateTask} style={styles.createForm}>
          <input
            type="text"
            placeholder="Что нужно сделать?..."
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            style={styles.input}
          />
          <button type="submit" style={styles.createButton}>Добавить задачу</button>
        </form>

        {/* Список задач */}
        <div style={styles.taskList}>
          {tasks.map(task => (
            <div key={task.id} style={styles.taskItem}>
              <span>{task.title}</span>
              <span style={styles.badge}>Доска #{task.board_id}</span>
            </div>
          ))}
          {tasks.length === 0 && <p style={{color: '#718096'}}>На этой доске пока нет задач.</p>}
        </div>
      </div>
    )
  }
}

// Стилизация дашборда
const styles = {
  container: { display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#f0f2f5', fontFamily: 'sans-serif' },
  card: { backgroundColor: '#fff', padding: '40px', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px' },
  title: { textAlign: 'center', marginBottom: '24px', color: '#1a202c' },
  form: { display: 'flex', flexDirection: 'column', gap: '16px' },
  inputGroup: { display: 'flex', flexDirection: 'column', gap: '6px' },
  label: { fontSize: '14px', color: '#4a5568', fontWeight: '500' },
  input: { padding: '10px 14px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '16px', outline: 'none', flex: 1 },
  button: { padding: '12px', backgroundColor: '#3182ce', color: '#fff', border: 'none', borderRadius: '6px', fontSize: '16px', cursor: 'pointer' },
  errorAlert: { backgroundColor: '#fed7d7', color: '#9b2c2c', padding: '10px', borderRadius: '6px', marginBottom: '16px', textAlign: 'center' },

  dashboardContainer: { padding: '40px', maxWidth: '900px', margin: '0 auto', fontFamily: 'sans-serif' },
  dashboardTitle: { color: '#2d3748', marginBottom: '24px' },
  createForm: { display: 'flex', gap: '12px', marginBottom: '32px' },
  createButton: { padding: '10px 20px', backgroundColor: '#48bb78', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '16px' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px' },
  boardCard: { backgroundColor: '#fff', padding: '20px', borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', cursor: 'pointer', transition: 'transform 0.2s', ':hover': { transform: 'translateY(-2px)' } },
  backButton: { padding: '8px 14px', backgroundColor: '#edf2f7', border: 'none', borderRadius: '6px', cursor: 'pointer', marginBottom: '16px', color: '#4a5568' },
  taskList: { display: 'flex', flexDirection: 'column', gap: '12px' },
  taskItem: { backgroundColor: '#fff', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  badge: { backgroundColor: '#e2e8f0', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', color: '#4a5568' }, // ЗАПЯТАЯ ТЕПЕРЬ ТУТ

  deleteButton: {
    position: 'absolute',
    top: '10px',
    right: '10px',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    fontSize: '18px',
    color: '#e53e3e',
    padding: '4px',
    lineHeight: '1',
    zIndex: 10, // Чтобы мусорка была поверх карточки
  },
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  modalContent: {
    backgroundColor: '#fff',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 8px 30px rgba(0,0,0,0.2)',
    textAlign: 'center',
    maxWidth: '350px',
    width: '90%',
  },
  modalActions: {
    display: 'flex',
    justifyContent: 'center',
    gap: '12px',
    marginTop: '20px',
  },
  confirmBtn: {
    backgroundColor: '#e53e3e',
    color: '#fff',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '16px',
  },
  cancelBtn: {
    backgroundColor: '#edf2f7',
    color: '#4a5568',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '16px',
  }
}

export default App