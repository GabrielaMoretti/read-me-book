// Main JavaScript for the home page
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupFileUpload();
    setupEventListeners();
}

function setupFileUpload() {
    const fileInput = document.getElementById('file-input');
    const uploadArea = document.getElementById('upload-area');
    const uploadBtn = document.getElementById('upload-btn');

    // File input change handler
    fileInput.addEventListener('change', handleFileSelect);

    // Upload button click handler
    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop handlers
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
}

function setupEventListeners() {
    // Close modal on background click
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });

    // ESC key to close modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect({ target: { files } });
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    
    if (!file) {
        return;
    }

    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showError('Apenas arquivos PDF são permitidos.');
        return;
    }

    if (file.size > 50 * 1024 * 1024) { // 50MB limit
        showError('O arquivo é muito grande. Limite máximo: 50MB.');
        return;
    }

    uploadFile(file);
}

async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        showLoading('Carregando e processando PDF...');

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success) {
            closeModal('loading-modal');
            showSuccess(`PDF processado com sucesso!\n${result.pages} páginas, ${result.chapters} capítulos encontrados.`);
            
            // Reload page to show new book
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            throw new Error(result.detail || 'Erro desconhecido');
        }
    } catch (error) {
        closeModal('loading-modal');
        showError(`Erro ao processar PDF: ${error.message}`);
    }
}

async function deleteBook(bookId) {
    if (!confirm('Tem certeza que deseja excluir este livro? Esta ação não pode ser desfeita.')) {
        return;
    }

    try {
        const response = await fetch(`/api/book/${bookId}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showSuccess('Livro excluído com sucesso!');
            
            // Remove book card from UI
            const bookCard = document.querySelector(`[data-book-id="${bookId}"]`);
            if (bookCard) {
                bookCard.remove();
            }

            // Check if library is empty
            const remainingBooks = document.querySelectorAll('.book-card');
            if (remainingBooks.length === 0) {
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }
        } else {
            throw new Error(result.detail || 'Erro ao excluir livro');
        }
    } catch (error) {
        showError(`Erro ao excluir livro: ${error.message}`);
    }
}

function showLoading(message = 'Carregando...') {
    const modal = document.getElementById('loading-modal');
    const messageEl = modal.querySelector('p');
    if (messageEl) {
        messageEl.textContent = message;
    }
    showModal('loading-modal');
}

function showError(message) {
    const modal = document.getElementById('error-modal');
    const messageEl = document.getElementById('error-message');
    if (messageEl) {
        messageEl.textContent = message;
    }
    showModal('error-modal');
}

function showSuccess(message) {
    const modal = document.getElementById('success-modal');
    const messageEl = document.getElementById('success-message');
    if (messageEl) {
        messageEl.textContent = message;
    }
    showModal('success-modal');
}

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }
}

function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    });
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Add click handlers to book cards
document.addEventListener('click', (e) => {
    const bookCard = e.target.closest('.book-card');
    if (bookCard && !e.target.closest('.book-actions')) {
        const bookId = bookCard.dataset.bookId;
        if (bookId) {
            window.location.href = `/reader/${bookId}`;
        }
    }
});