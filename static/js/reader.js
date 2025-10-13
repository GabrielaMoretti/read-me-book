// Reader JavaScript for book reading interface
document.addEventListener('DOMContentLoaded', function() {
    initializeReader();
});

let currentChapter = 0;
let isReading = false;
let currentSpeech = null;
let readingPosition = 0;

function initializeReader() {
    currentChapter = window.bookData.current_chapter || 0;
    
    setupReaderControls();
    setupChapterNavigation();
    setupTextControls();
    setupAnnotations();
    updateChapterDisplay();
    
    // Load settings from localStorage
    loadUserSettings();
}

function setupReaderControls() {
    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const stopBtn = document.getElementById('stop-btn');
    const speedSlider = document.getElementById('speed-slider');
    const speedValue = document.getElementById('speed-value');

    playBtn.addEventListener('click', startReading);
    pauseBtn.addEventListener('click', pauseReading);
    stopBtn.addEventListener('click', stopReading);

    speedSlider.addEventListener('input', (e) => {
        const speed = parseFloat(e.target.value);
        speedValue.textContent = speed.toFixed(1) + 'x';
        updateSpeechSpeed(speed);
        
        // Save speed preference
        localStorage.setItem('readingSpeed', speed);
    });

    // Load saved speed
    const savedSpeed = localStorage.getItem('readingSpeed') || '1.0';
    speedSlider.value = savedSpeed;
    speedValue.textContent = parseFloat(savedSpeed).toFixed(1) + 'x';
}

function setupChapterNavigation() {
    const chapterItems = document.querySelectorAll('.chapter-item');
    const prevBtn = document.getElementById('prev-chapter');
    const nextBtn = document.getElementById('next-chapter');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('chapter-sidebar');

    chapterItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            selectChapter(index);
        });
    });

    prevBtn.addEventListener('click', () => {
        if (currentChapter > 0) {
            selectChapter(currentChapter - 1);
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentChapter < window.bookData.chapters.length - 1) {
            selectChapter(currentChapter + 1);
        }
    });

    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        const icon = sidebarToggle.querySelector('i');
        if (sidebar.classList.contains('collapsed')) {
            icon.className = 'fas fa-chevron-right';
        } else {
            icon.className = 'fas fa-chevron-left';
        }
    });

    // Mobile sidebar toggle
    if (window.innerWidth <= 768) {
        sidebar.classList.add('collapsed');
        
        // Show sidebar on mobile when chapter item is clicked
        chapterItems.forEach(item => {
            item.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    sidebar.classList.add('collapsed');
                }
            });
        });
    }
}

function setupTextControls() {
    const fontSizeBtn = document.getElementById('font-size-btn');
    const addAnnotationBtn = document.getElementById('add-annotation-btn');
    const toggleAnnotationsBtn = document.getElementById('toggle-annotations-btn');
    const fontSizeModal = document.getElementById('font-size-modal');
    const fontSizeRange = document.getElementById('font-size-range');
    const lineHeightRange = document.getElementById('line-height-range');
    const fontSizeDisplay = document.getElementById('font-size-display');
    const lineHeightDisplay = document.getElementById('line-height-display');

    fontSizeBtn.addEventListener('click', () => {
        showModal('font-size-modal');
    });

    addAnnotationBtn.addEventListener('click', () => {
        showModal('annotation-modal');
    });

    toggleAnnotationsBtn.addEventListener('click', () => {
        toggleAnnotationsPanel();
    });

    // Font size controls
    fontSizeRange.addEventListener('input', (e) => {
        const fontSize = e.target.value + 'px';
        document.getElementById('text-content').style.fontSize = fontSize;
        fontSizeDisplay.textContent = fontSize;
        localStorage.setItem('fontSize', e.target.value);
    });

    lineHeightRange.addEventListener('input', (e) => {
        const lineHeight = e.target.value;
        document.getElementById('text-content').style.lineHeight = lineHeight;
        lineHeightDisplay.textContent = lineHeight;
        localStorage.setItem('lineHeight', lineHeight);
    });

    // Close modals
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

function setupAnnotations() {
    const annotationForm = document.getElementById('annotation-form');
    const closeAnnotations = document.getElementById('close-annotations');

    annotationForm.addEventListener('submit', saveAnnotation);
    
    closeAnnotations.addEventListener('click', () => {
        toggleAnnotationsPanel();
    });

    // Load annotations for current chapter
    loadAnnotations();
}

function selectChapter(chapterIndex) {
    if (chapterIndex < 0 || chapterIndex >= window.bookData.chapters.length) {
        return;
    }

    // Stop current reading
    if (isReading) {
        stopReading();
    }

    currentChapter = chapterIndex;
    
    // Update UI
    updateChapterDisplay();
    updateNavigationButtons();
    
    // Update active chapter in sidebar
    document.querySelectorAll('.chapter-item').forEach((item, index) => {
        item.classList.toggle('active', index === chapterIndex);
    });

    // Load chapter content and annotations
    loadChapterContent();
    loadAnnotations();
}

function updateChapterDisplay() {
    const chapter = window.bookData.chapters[currentChapter];
    if (!chapter) return;

    document.getElementById('current-chapter-num').textContent = currentChapter + 1;
    document.getElementById('current-chapter-title').textContent = chapter.title;
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-chapter');
    const nextBtn = document.getElementById('next-chapter');

    prevBtn.disabled = currentChapter === 0;
    nextBtn.disabled = currentChapter === window.bookData.chapters.length - 1;
}

async function loadChapterContent() {
    try {
        const response = await fetch(`/api/book/${window.bookData.id}/chapter/${currentChapter}`);
        const data = await response.json();

        if (response.ok) {
            const textContent = document.getElementById('text-content');
            textContent.innerHTML = data.chapter.content.replace(/\n/g, '<br>');
        }
    } catch (error) {
        console.error('Error loading chapter content:', error);
    }
}

async function startReading() {
    if (isReading) return;

    const textContent = document.getElementById('text-content').textContent;
    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');

    if ('speechSynthesis' in window) {
        isReading = true;
        playBtn.style.display = 'none';
        pauseBtn.style.display = 'flex';

        // Create speech utterance
        currentSpeech = new SpeechSynthesisUtterance(textContent);
        
        // Set speech properties
        const speed = parseFloat(document.getElementById('speed-slider').value);
        currentSpeech.rate = speed;
        currentSpeech.pitch = 1;
        currentSpeech.volume = 1;

        // Event handlers
        currentSpeech.onend = () => {
            stopReading();
            // Auto-advance to next chapter if available
            if (currentChapter < window.bookData.chapters.length - 1) {
                setTimeout(() => {
                    selectChapter(currentChapter + 1);
                    startReading();
                }, 1000);
            }
        };

        currentSpeech.onerror = (e) => {
            console.error('Speech synthesis error:', e);
            stopReading();
        };

        // Start speaking
        speechSynthesis.speak(currentSpeech);
        
        // Send to backend for logging
        try {
            await fetch('/api/tts/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: textContent })
            });
        } catch (error) {
            console.error('Error logging TTS request:', error);
        }
    } else {
        alert('Text-to-speech não é suportado neste navegador.');
    }
}

function pauseReading() {
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
    }
    
    isReading = false;
    document.getElementById('play-btn').style.display = 'flex';
    document.getElementById('pause-btn').style.display = 'none';
}

function stopReading() {
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
    }
    
    isReading = false;
    currentSpeech = null;
    readingPosition = 0;
    
    document.getElementById('play-btn').style.display = 'flex';
    document.getElementById('pause-btn').style.display = 'none';
}

function updateSpeechSpeed(speed) {
    if (currentSpeech && speechSynthesis.speaking) {
        // Unfortunately, we can't change speed mid-speech in most browsers
        // Would need to stop and restart
    }
}

async function saveAnnotation(e) {
    e.preventDefault();
    
    const annotationText = document.getElementById('annotation-text').value.trim();
    if (!annotationText) return;

    try {
        const chapterId = window.bookData.chapters[currentChapter].id;
        
        const response = await fetch(`/api/book/${window.bookData.id}/chapter/${chapterId}/annotation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: annotationText,
                position: readingPosition
            })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            document.getElementById('annotation-text').value = '';
            closeModal('annotation-modal');
            loadAnnotations(); // Reload annotations
            
            // Show success message
            showTemporaryMessage('Anotação salva com sucesso!', 'success');
        } else {
            throw new Error(result.detail || 'Erro ao salvar anotação');
        }
    } catch (error) {
        console.error('Error saving annotation:', error);
        showTemporaryMessage('Erro ao salvar anotação: ' + error.message, 'error');
    }
}

async function loadAnnotations() {
    try {
        const chapterId = window.bookData.chapters[currentChapter].id;
        const response = await fetch(`/api/book/${window.bookData.id}/chapter/${currentChapter}`);
        const data = await response.json();

        if (response.ok) {
            displayAnnotations(data.annotations);
        }
    } catch (error) {
        console.error('Error loading annotations:', error);
    }
}

function displayAnnotations(annotations) {
    const annotationsList = document.getElementById('annotations-list');
    
    if (annotations.length === 0) {
        annotationsList.innerHTML = '<p class="no-annotations">Nenhuma anotação neste capítulo.</p>';
        return;
    }

    annotationsList.innerHTML = annotations.map(annotation => `
        <div class="annotation-item">
            <div class="annotation-text">${annotation.text}</div>
            <div class="annotation-meta">
                <i class="fas fa-clock"></i>
                ${formatDate(annotation.created_date)}
            </div>
        </div>
    `).join('');
}

function toggleAnnotationsPanel() {
    const panel = document.getElementById('annotations-panel');
    const btn = document.getElementById('toggle-annotations-btn');
    
    panel.classList.toggle('show');
    btn.classList.toggle('active');
    
    if (panel.classList.contains('show')) {
        loadAnnotations();
    }
}

function loadUserSettings() {
    // Load font size
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.getElementById('text-content').style.fontSize = savedFontSize + 'px';
        document.getElementById('font-size-range').value = savedFontSize;
        document.getElementById('font-size-display').textContent = savedFontSize + 'px';
    }

    // Load line height
    const savedLineHeight = localStorage.getItem('lineHeight');
    if (savedLineHeight) {
        document.getElementById('text-content').style.lineHeight = savedLineHeight;
        document.getElementById('line-height-range').value = savedLineHeight;
        document.getElementById('line-height-display').textContent = savedLineHeight;
    }
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

function showTemporaryMessage(message, type = 'info') {
    const messageEl = document.createElement('div');
    messageEl.className = `temporary-message ${type}`;
    messageEl.textContent = message;
    
    messageEl.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1001;
        animation: slideInRight 0.3s ease;
    `;
    
    if (type === 'success') {
        messageEl.style.background = '#27ae60';
    } else if (type === 'error') {
        messageEl.style.background = '#e74c3c';
    } else {
        messageEl.style.background = '#3498db';
    }
    
    document.body.appendChild(messageEl);
    
    setTimeout(() => {
        messageEl.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.parentNode.removeChild(messageEl);
            }
        }, 300);
    }, 3000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') {
        return;
    }

    switch (e.key) {
        case ' ':
            e.preventDefault();
            if (isReading) {
                pauseReading();
            } else {
                startReading();
            }
            break;
        case 'ArrowLeft':
            if (currentChapter > 0) {
                selectChapter(currentChapter - 1);
            }
            break;
        case 'ArrowRight':
            if (currentChapter < window.bookData.chapters.length - 1) {
                selectChapter(currentChapter + 1);
            }
            break;
        case 'n':
            showModal('annotation-modal');
            break;
        case 'a':
            toggleAnnotationsPanel();
            break;
    }
});

// Add CSS animations for temporary messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .no-annotations {
        text-align: center;
        color: #666;
        font-style: italic;
        padding: 2rem;
    }
`;
document.head.appendChild(style);