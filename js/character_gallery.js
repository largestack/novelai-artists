/**
 * Character Gallery JS - For NovelAI Character Galleries
 * Refactored for clarity and bug fixes.
 */

const AGE_DISCLAIMER_KEY = 'ageDisclaimerAccepted_v1';
const THEME_KEY = 'site_theme_v1';
const HEADER_REVEAL_THRESHOLD_PX = 250;

document.addEventListener('DOMContentLoaded', function() {

    // --- Global Setup (Theme & Header Scroll) ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const bodyEl = document.body;
    const headerEl = document.querySelector('header');

    function applyTheme(theme) {
        if (theme === 'dark') {
            bodyEl.classList.add('dark-mode');
            if (themeToggleBtn) themeToggleBtn.textContent = '☀️';
        } else {
            bodyEl.classList.remove('dark-mode');
            if (themeToggleBtn) themeToggleBtn.textContent = '🌙';
        }
    }

    let savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
    applyTheme(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const newTheme = bodyEl.classList.contains('dark-mode') ? 'light' : 'dark';
            localStorage.setItem(THEME_KEY, newTheme);
            applyTheme(newTheme);
        });
    }

    let lastScrollTop = 0;
    let upwardScrollDistance = 0;
    window.addEventListener('scroll', function() {
        if (!headerEl || window.innerWidth >= 768) return;
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop) {
            if (scrollTop > headerEl.offsetHeight) headerEl.classList.add('header-hidden');
            upwardScrollDistance = 0;
        } else if (scrollTop < lastScrollTop) {
            upwardScrollDistance += lastScrollTop - scrollTop;
            if (upwardScrollDistance > HEADER_REVEAL_THRESHOLD_PX || scrollTop <= headerEl.offsetHeight) {
                headerEl.classList.remove('header-hidden');
            }
        }
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    }, false);


    // --- Gallery Logic ---
    function showAgeDisclaimer() {
        const overlay = document.getElementById('age-disclaimer-overlay');
        const confirmBtn = document.getElementById('age-confirm-button');
        const exitBtn = document.getElementById('age-exit-button');

        if (!overlay || !confirmBtn || !exitBtn) {
            document.body.innerHTML = "<p style='text-align:center; padding-top: 50px;'>Error: Age verification components are missing.</p>";
            return;
        }

        overlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        confirmBtn.onclick = () => {
            localStorage.setItem(AGE_DISCLAIMER_KEY, 'true');
            overlay.style.display = 'none';
            document.body.style.overflow = '';
            initializeGallery();
        };
        exitBtn.onclick = () => {
            window.location.href = 'index.html';
        };
    }

    function initializeGallery() {
        const galleryEl = document.getElementById('gallery');
        const lightboxEl = document.getElementById('lightbox');
        const lightboxImgEl = document.getElementById('lightbox-img');
        const lightboxArtistEl = document.getElementById('lightbox-artist');
        const lightboxModelEl = document.getElementById('lightbox-model');
        const lightboxSeedEl = document.getElementById('lightbox-seed');
        const lightboxRelatedImagesContainer = document.getElementById('lightbox-related-images');
        const favoriteButtonEl = document.getElementById('favorite-button');
        const favoritesToggleBtn = document.getElementById('favorites-toggle');
        const closeBtn = document.querySelector('.lightbox .close');
        const templateTextEl = document.getElementById('template-text');
        const modelSelectorEl = document.getElementById('model-selector');
        const loadingEl = document.getElementById('loading');
        const searchBoxEl = document.getElementById('search-box');
        const fullscreenOverlay = document.getElementById('fullscreen-overlay');
        const fullscreenImg = document.getElementById('fullscreen-img');
        const lightboxPromptArea = document.getElementById('lightbox-prompt-area');

        if (!galleryEl || !lightboxEl || !modelSelectorEl || !lightboxPromptArea) {
            console.error("Essential gallery elements are missing. Check HTML structure.");
            return;
        }
        
        if (templateTextEl) {
            templateTextEl.textContent = galleryData.template;
        }
        
        const FAVORITES_KEY = `nai-favorites-${galleryData.section}`;
        let favorites = new Set(JSON.parse(localStorage.getItem(FAVORITES_KEY) || '[]'));
        let showingFavorites = false;
        let currentSearchTerm = '';
        
        const imagesByModel = {};
        const modelNameMap = {};
        let allModels = new Set();
        
        galleryData.sectionImages.forEach(img => {
            if (!imagesByModel[img.model]) imagesByModel[img.model] = [];
            imagesByModel[img.model].push(img);
            allModels.add(img.model);
            modelNameMap[img.model] = img.modelName || img.model;
        });

        if (modelSelectorEl) {
            const sortedModels = [...allModels].sort((a,b) => (modelNameMap[a] || "").localeCompare(modelNameMap[b] || ""));
            modelSelectorEl.innerHTML = `<button class="model-button active" data-model="all">All Models</button>` +
            sortedModels.map(model => 
                `<button class="model-button" data-model="${model}">${modelNameMap[model]}</button>`
            ).join('');

            modelSelectorEl.addEventListener('click', (e) => {
                if (e.target.matches('.model-button')) {
                    modelSelectorEl.querySelectorAll('.model-button').forEach(btn => btn.classList.remove('active'));
                    e.target.classList.add('active');
                    filterGallery();
                }
            });
        }
        
        function showToast(message) {
            let toast = document.getElementById('copy-toast-notification'); 
            if (!toast) {
                toast = document.createElement('div');
                toast.id = 'copy-toast-notification';
                toast.className = 'copy-toast'; 
                document.body.appendChild(toast);
            }
            toast.textContent = message;
            toast.classList.add('visible');
            setTimeout(() => { toast.classList.remove('visible'); }, 2000);
        }
        
        function toggleFavorite(imageId) {
            const imageIdStr = String(imageId);
            if (favorites.has(imageIdStr)) {
                favorites.delete(imageIdStr);
            } else {
                favorites.add(imageIdStr);
            }
            localStorage.setItem(FAVORITES_KEY, JSON.stringify([...favorites]));
            updateCardFavoriteIcon(imageIdStr);
            if (currentLightboxImage && String(currentLightboxImage.id) === imageIdStr) {
                updateLightboxFavoriteButton();
            }
            if (showingFavorites && !favorites.has(imageIdStr)) {
                const card = galleryEl.querySelector(`.image-card[data-id="${imageIdStr}"]`);
                if(card) card.remove();
            }
        }
        
        function updateCardFavoriteIcon(imageId) {
             const cardIcon = galleryEl.querySelector(`.image-card[data-id="${imageId}"] .favorite-icon-card`);
             if (cardIcon) cardIcon.classList.toggle('favorited', favorites.has(imageId));
        }

        function updateLightboxFavoriteButton() {
            if (!favoriteButtonEl || !currentLightboxImage) return;
            const isFavorite = favorites.has(String(currentLightboxImage.id));
            favoriteButtonEl.classList.toggle('favorited', isFavorite);
            favoriteButtonEl.querySelector('#favorite-text').textContent = isFavorite ? 'Remove from Favorites' : 'Add to Favorites';
        }
        
        if (favoritesToggleBtn) {
            favoritesToggleBtn.addEventListener('click', function() {
                showingFavorites = !showingFavorites;
                this.textContent = showingFavorites ? 'Show All' : 'Show Favorites';
                this.classList.toggle('active-filter', showingFavorites);
                filterGallery();
            });
        }

        if (searchBoxEl) {
            searchBoxEl.addEventListener('input', () => {
                currentSearchTerm = searchBoxEl.value.toLowerCase().trim();
                clearTimeout(searchBoxEl.searchTimeout);
                searchBoxEl.searchTimeout = setTimeout(filterGallery, 300);
            });
        }
        
        let shuffledImages = [];
        let loadedImagesCount = 0;
        let currentLightboxImage = null;

        function filterGallery() {
            const activeModelButton = modelSelectorEl.querySelector('.model-button.active');
            const model = activeModelButton ? activeModelButton.dataset.model : 'all';
            
            let filtered = (model === 'all') ? [...galleryData.sectionImages] : (imagesByModel[model] || []);
            if (showingFavorites) {
                filtered = filtered.filter(img => favorites.has(String(img.id)));
            }
            if (currentSearchTerm) {
                filtered = filtered.filter(img => 
                    (img.artist && img.artist.toLowerCase().includes(currentSearchTerm)) ||
                    (img.prompt && img.prompt.toLowerCase().includes(currentSearchTerm)) ||
                    ('character1' in img && img.character1.toLowerCase().includes(currentSearchTerm)) ||
                    ('character2' in img && img.character2.toLowerCase().includes(currentSearchTerm))
                );
            }
            
            shuffledImages = filtered.sort(() => 0.5 - Math.random());
            galleryEl.innerHTML = '';
            loadedImagesCount = 0;
            loadImages(24);
        }
        
        function loadImages(count) {
            if (loadedImagesCount >= shuffledImages.length) {
                if (loadingEl) loadingEl.style.display = 'none';
                return;
            }

            const fragment = document.createDocumentFragment();
            const endIndex = Math.min(loadedImagesCount + count, shuffledImages.length);
            for (let i = loadedImagesCount; i < endIndex; i++) {
                const img = shuffledImages[i];
                const card = document.createElement('div');
                card.className = 'image-card';
                card.dataset.id = img.id;
                card.innerHTML = `
                    <div class="image-container">
                        <div class="favorite-icon-card ${favorites.has(String(img.id)) ? 'favorited' : ''}"></div>
                        <img src="${galleryData.imagePaths.thumb}${img.id}.jpg" alt="Gallery thumbnail" loading="lazy">
                    </div>`;
                card.querySelector('.favorite-icon-card').addEventListener('click', (e) => { e.stopPropagation(); toggleFavorite(img.id); });
                card.addEventListener('click', () => openLightbox(img));
                fragment.appendChild(card);
            }
            galleryEl.appendChild(fragment);
            loadedImagesCount = endIndex;
            if (loadingEl) loadingEl.style.display = loadedImagesCount < shuffledImages.length ? 'block' : 'none';
        }
        
        function openLightbox(img) {
            currentLightboxImage = img;
            document.querySelector('.lightbox-content').scrollTop = 0;
            lightboxImgEl.src = `${galleryData.imagePaths.full}${img.id}.jpg`;
            
            lightboxPromptArea.innerHTML = ''; // Clear previous content

            const createPromptBlock = (title, text) => {
                const pre = document.createElement('pre');
                pre.textContent = text;
                const button = document.createElement('button');
                button.className = 'copy-button';
                button.textContent = `Copy ${title}`;
                button.onclick = () => navigator.clipboard.writeText(text).then(() => showToast(`${title} copied!`));
                
                const container = document.createElement('div');
                container.className = 'prompt-container';
                container.innerHTML = `<h4>${title}</h4>`;
                container.appendChild(pre);
                container.appendChild(button);
                return container;
            };

            /*** BUG FIX: Conditional prompt display ***/
            if ('character1' in img && 'character2' in img) {
                // V4 Style (noncon)
                lightboxPromptArea.appendChild(createPromptBlock('Scene Prompt', img.prompt));
                lightboxPromptArea.appendChild(createPromptBlock('Character 1', img.character1));
                lightboxPromptArea.appendChild(createPromptBlock('Character 2', img.character2));
            } else {
                // V3 Style (standard galleries)
                 lightboxPromptArea.appendChild(createPromptBlock('Full Prompt', img.prompt));
            }

            lightboxArtistEl.textContent = img.artist;
            lightboxModelEl.textContent = img.modelName;
            lightboxSeedEl.textContent = img.seed;
            updateLightboxFavoriteButton();
            
            lightboxRelatedImagesContainer.innerHTML = ''; // Clear and rebuild related images
            const relatedImages = galleryData.sectionImages
                .filter(rel => rel.id !== img.id && rel.artist === img.artist && rel.model === img.model)
                .slice(0, 8);
            
            if (relatedImages.length > 0) {
                const relatedGrid = document.createElement('div');
                relatedGrid.className = 'related-images-grid';
                relatedGrid.innerHTML = relatedImages.map(relImg => `
                    <img src="${galleryData.imagePaths.thumb}${relImg.id}.jpg" 
                         alt="Related thumbnail" 
                         class="related-image ${favorites.has(String(relImg.id)) ? 'favorited' : ''}" 
                         data-related-id="${relImg.id}">
                `).join('');
                lightboxRelatedImagesContainer.innerHTML = '<h4>More from this artist & model:</h4>';
                lightboxRelatedImagesContainer.appendChild(relatedGrid);
            }

            lightboxEl.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        function closeLightbox() {
            lightboxEl.classList.remove('active');
            lightboxImgEl.src = '';
            currentLightboxImage = null;
            document.body.style.overflow = '';
        }
        
        // --- Event Listeners ---
        favoriteButtonEl.addEventListener('click', () => { if (currentLightboxImage) toggleFavorite(currentLightboxImage.id); });
        lightboxImgEl.addEventListener('click', () => { fullscreenImg.src = lightboxImgEl.src; fullscreenOverlay.classList.add('visible'); });
        fullscreenOverlay.addEventListener('click', () => fullscreenOverlay.classList.remove('visible'));
        closeBtn.addEventListener('click', closeLightbox);
        lightboxEl.addEventListener('click', (e) => { if (e.target === lightboxEl) closeLightbox(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && lightboxEl.classList.contains('active')) closeLightbox(); });
        window.addEventListener('scroll', () => {
            if (loadingEl.style.display !== 'none' && window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 500) {
                loadImages(12);
            }
        });
        lightboxArtistEl.addEventListener('click', () => {
             if (currentLightboxImage && currentLightboxImage.artist) {
                navigator.clipboard.writeText(currentLightboxImage.artist).then(() => showToast(`Copied artist!`));
             }
        });
        lightboxRelatedImagesContainer.addEventListener('click', (e) => {
            if(e.target.matches('.related-image')) {
                const relatedId = e.target.dataset.relatedId;
                const relatedImgObject = galleryData.sectionImages.find(img => String(img.id) === relatedId);
                if (relatedImgObject) openLightbox(relatedImgObject);
            }
        });
        
        // Initial load
        filterGallery();
    }

    function mainInit() {
        if (typeof galleryData === 'undefined' || !galleryData.sectionImages) {
            console.error("galleryData is not defined. Cannot initialize gallery.");
            document.body.innerHTML = 'Error: Gallery data is missing.';
            return;
        }
        const disclaimerAccepted = localStorage.getItem(AGE_DISCLAIMER_KEY) === 'true';
        if (galleryData.isNsfwSection && !disclaimerAccepted) {
            showAgeDisclaimer();
        } else {
            initializeGallery();
        }
    }

    mainInit();
});
