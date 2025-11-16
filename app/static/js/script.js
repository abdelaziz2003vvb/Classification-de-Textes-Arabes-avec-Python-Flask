/**
 * Script JavaScript pour l'interface de Classification de Textes Arabes
 * Location: src/main/resources/static/js/script.js
 */

// ============================================
// 1. Initialisation au chargement de la page
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('📱 Interface de Classification chargée');

    // Initialiser toutes les fonctionnalités
    initFileUpload();
    initTextArea();
    initFormValidation();
    initAnimations();
    initCharts();
    initTooltips();

    // Auto-hide alerts après 5 secondes
    autoHideAlerts();

    // Ajouter les événements de confirmation
    addConfirmationDialogs();
});

// ============================================
// 2. Gestion de l'upload de fichiers
// ============================================
function initFileUpload() {
    const fileInput = document.getElementById('file');

    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if (file) {
                // Vérifier le type de fichier
                if (!file.name.endsWith('.txt')) {
                    showAlert('Erreur: Seuls les fichiers .txt sont acceptés', 'error');
                    fileInput.value = '';
                    return;
                }

                // Vérifier la taille (max 10MB)
                if (file.size > 10 * 1024 * 1024) {
                    showAlert('Erreur: Le fichier est trop volumineux (max 10MB)', 'error');
                    fileInput.value = '';
                    return;
                }

                // Afficher le nom du fichier
                showFileInfo(file);

                // Prévisualiser le contenu
                previewFileContent(file);
            }
        });

        // Drag and drop
        const fileInputContainer = fileInput.parentElement;

        fileInputContainer.addEventListener('dragover', function(e) {
            e.preventDefault();
            fileInputContainer.classList.add('dragover');
        });

        fileInputContainer.addEventListener('dragleave', function(e) {
            e.preventDefault();
            fileInputContainer.classList.remove('dragover');
        });

        fileInputContainer.addEventListener('drop', function(e) {
            e.preventDefault();
            fileInputContainer.classList.remove('dragover');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    }
}

// Afficher les informations du fichier
function showFileInfo(file) {
    const fileSize = formatFileSize(file.size);
    const fileInfo = document.createElement('div');
    fileInfo.className = 'file-info';
    fileInfo.innerHTML = `
        <span class="file-icon">📄</span>
        <span class="file-name">${file.name}</span>
        <span class="file-size">${fileSize}</span>
    `;

    // Supprimer l'ancienne info si elle existe
    const oldInfo = document.querySelector('.file-info');
    if (oldInfo) oldInfo.remove();

    // Ajouter la nouvelle info
    const fileInput = document.getElementById('file');
    fileInput.parentElement.appendChild(fileInfo);
}

// Prévisualiser le contenu du fichier
function previewFileContent(file) {
    const reader = new FileReader();

    reader.onload = function(e) {
        const content = e.target.result;
        const preview = document.getElementById('file-preview');

        if (preview) {
            preview.style.display = 'block';
            preview.innerHTML = `
                <h4>Aperçu du contenu:</h4>
                <pre dir="rtl">${content.substring(0, 500)}${content.length > 500 ? '...' : ''}</pre>
            `;
        }
    };

    reader.readAsText(file, 'UTF-8');
}

// Formater la taille du fichier
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ============================================
// 3. Gestion de la zone de texte
// ============================================
function initTextArea() {
    const textArea = document.getElementById('text');

    if (textArea) {
        // Compter les caractères
        const charCounter = document.createElement('div');
        charCounter.className = 'char-counter';
        charCounter.textContent = '0 caractères';
        textArea.parentElement.appendChild(charCounter);

        textArea.addEventListener('input', function() {
            const count = this.value.length;
            charCounter.textContent = `${count} caractère${count > 1 ? 's' : ''}`;

            // Changer la couleur si trop court
            if (count < 10 && count > 0) {
                charCounter.style.color = '#ff9800';
            } else {
                charCounter.style.color = '#666';
            }
        });

        // Auto-resize
        textArea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
}

// ============================================
// 4. Validation des formulaires
// ============================================
function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');

            if (submitBtn) {
                // Désactiver le bouton et afficher le loading
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading"></span> Traitement en cours...';

                // Si validation échoue, réactiver
                if (!validateForm(form)) {
                    e.preventDefault();
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.dataset.originalText || 'Classifier';
                }
            }
        });
    });
}

function validateForm(form) {
    // Validation du fichier
    const fileInput = form.querySelector('input[type="file"]');
    if (fileInput && fileInput.required) {
        if (!fileInput.files || fileInput.files.length === 0) {
            showAlert('Veuillez sélectionner un fichier', 'error');
            return false;
        }
    }

    // Validation du textarea
    const textArea = form.querySelector('textarea');
    if (textArea && textArea.required) {
        if (!textArea.value.trim()) {
            showAlert('Le texte ne peut pas être vide', 'error');
            return false;
        }
        if (textArea.value.trim().length < 10) {
            showAlert('Le texte doit contenir au moins 10 caractères', 'error');
            return false;
        }
    }

    return true;
}

// ============================================
// 5. Animations et effets visuels
// ============================================
function initAnimations() {
    // Animation des barres de probabilité
    const probBars = document.querySelectorAll('.prob-bar');

    probBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';

        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });

    // Animation des statistiques
    animateNumbers();

    // Effet hover sur les cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        });
    });
}

// Animer les chiffres (compteur)
function animateNumbers() {
    const statValues = document.querySelectorAll('.stat-value');

    statValues.forEach(element => {
        const finalValue = parseInt(element.textContent);
        if (!isNaN(finalValue)) {
            let currentValue = 0;
            const increment = finalValue / 50;

            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    element.textContent = finalValue;
                    clearInterval(timer);
                } else {
                    element.textContent = Math.floor(currentValue);
                }
            }, 20);
        }
    });
}

// ============================================
// 6. Graphiques et visualisations
// ============================================
function initCharts() {
    // Ajouter un graphique pour la matrice de confusion si disponible
    const confusionMatrix = document.querySelector('.confusion-matrix');

    if (confusionMatrix) {
        visualizeConfusionMatrix(confusionMatrix);
    }

    // Graphique des probabilités (déjà géré en CSS, mais on peut améliorer)
    enhanceProbabilityBars();
}

function enhanceProbabilityBars() {
    const probItems = document.querySelectorAll('.probability-item');

    probItems.forEach(item => {
        const bar = item.querySelector('.prob-bar');
        const value = item.querySelector('.prob-value');

        if (bar && value) {
            // Ajouter un effet au survol
            item.addEventListener('mouseenter', function() {
                bar.style.transform = 'scaleY(1.1)';
                value.style.fontWeight = 'bold';
            });

            item.addEventListener('mouseleave', function() {
                bar.style.transform = 'scaleY(1)';
                value.style.fontWeight = 'normal';
            });
        }
    });
}

// ============================================
// 7. Alertes et notifications
// ============================================
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <strong>${type === 'error' ? '❌' : '✅'}</strong>
        <span>${message}</span>
        <button class="alert-close" onclick="this.parentElement.remove()">×</button>
    `;

    // Insérer au début du container
    const container = document.querySelector('.container');
    const header = container.querySelector('header');
    container.insertBefore(alert, header.nextSibling);

    // Auto-hide après 5 secondes
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

// ============================================
// 8. Tooltips
// ============================================
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
            tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
        });

        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}

// ============================================
// 9. Dialogues de confirmation
// ============================================
function addConfirmationDialogs() {
    // Confirmation avant entraînement
    const trainButtons = document.querySelectorAll('form[action*="train"] button[type="submit"]');

    trainButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const confirmed = confirm('Voulez-vous entraîner le modèle? Cela peut prendre quelques secondes.');
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
}

// ============================================
// 10. Copier le texte dans le presse-papiers
// ============================================
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Texte copié dans le presse-papiers!', 'success');
    }).catch(err => {
        console.error('Erreur lors de la copie:', err);
    });
}

// Ajouter des boutons de copie pour les résultats
document.addEventListener('DOMContentLoaded', function() {
    const documentContent = document.querySelector('.document-content pre');

    if (documentContent) {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn-copy';
        copyBtn.innerHTML = '📋 Copier';
        copyBtn.onclick = function() {
            copyToClipboard(documentContent.textContent);
        };

        documentContent.parentElement.insertBefore(copyBtn, documentContent);
    }
});

// ============================================
// 11. Exporter les résultats
// ============================================
function exportResults() {
    const results = {
        category: document.querySelector('.category-badge')?.textContent,
        confidence: document.querySelector('.confidence-badge')?.textContent,
        probabilities: {},
        content: document.querySelector('.document-content pre')?.textContent
    };

    // Récupérer les probabilités
    document.querySelectorAll('.probability-item').forEach(item => {
        const label = item.querySelector('.prob-label').textContent;
        const value = item.querySelector('.prob-value').textContent;
        results.probabilities[label] = value;
    });

    // Créer un blob et télécharger
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url;
    link.download = 'classification-result.json';
    link.click();

    showAlert('Résultats exportés!', 'success');
}

// Ajouter un bouton d'export sur la page de résultats
document.addEventListener('DOMContentLoaded', function() {
    const resultCard = document.querySelector('.result-card');

    if (resultCard) {
        const exportBtn = document.createElement('button');
        exportBtn.className = 'btn btn-secondary';
        exportBtn.innerHTML = '💾 Exporter les Résultats';
        exportBtn.onclick = exportResults;

        const buttonGroup = document.querySelector('.button-group');
        if (buttonGroup) {
            buttonGroup.appendChild(exportBtn);
        }
    }
});

// ============================================
// 12. Mode sombre/clair (bonus)
// ============================================
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
}

// Charger la préférence au démarrage
document.addEventListener('DOMContentLoaded', function() {
    const darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
});

// ============================================
// 13. Recherche et filtrage (si plusieurs résultats)
// ============================================
function filterCategories(searchText) {
    const categories = document.querySelectorAll('.categories li');

    categories.forEach(category => {
        const text = category.textContent.toLowerCase();
        if (text.includes(searchText.toLowerCase())) {
            category.style.display = 'block';
        } else {
            category.style.display = 'none';
        }
    });
}

// ============================================
// 14. Impression des résultats
// ============================================
function printResults() {
    window.print();
}

// ============================================
// 15. Raccourcis clavier
// ============================================
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter pour soumettre le formulaire
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeForm = document.activeElement.closest('form');
        if (activeForm) {
            activeForm.submit();
        }
    }

    // Échap pour fermer les alertes
    if (e.key === 'Escape') {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => alert.remove());
    }
});

// ============================================
// 16. Utilitaires
// ============================================

// Formater les pourcentages
function formatPercent(value) {
    return (value * 100).toFixed(2) + '%';
}

// Vérifier si l'élément est visible
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Smooth scroll vers un élément
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// ============================================
// 17. Console d'information
// ============================================
console.log(`
╔════════════════════════════════════════════╗
║  Classification de Textes Arabes          ║
║  Naive Bayes + SAFAR                      ║
║                                            ║
║  Version: 1.0.0                           ║
║  Port: 8082                               ║
║  Status: ✅ Ready                          ║
╚════════════════════════════════════════════╝
`);

// ============================================
// Exports (si utilisé comme module)
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showAlert,
        copyToClipboard,
        exportResults,
        formatPercent
    };
}