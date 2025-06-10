/**
 * Character Gallery JS - For NovelAI Character Galleries
 */

const GALLERY_IMAGE_THUMB_SCALE_PERCENT = 100;
const THUMB_PATH = "https://f005.backblazeb2.com/file/novelai-images/thumb/";
const FULL_PATH = "https://f005.backblazeb2.com/file/novelai-images/full/";
const AGE_DISCLAIMER_KEY = 'ageDisclaimerAccepted_v1';
const THEME_KEY = 'site_theme_v1';
const HEADER_REVEAL_THRESHOLD_PX = 250; // Approx 3 small images. Adjust as needed.

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
            const modalContent = document.getElementById('age-disclaimer-modal');
            if (modalContent) modalContent.innerHTML = '<h2>Access Denied</h2><p>You must be 18 or older to view this content.</p>';
        };
    }

    function initializeGallery() {
        const galleryEl = document.getElementById('gallery');
        const lightboxEl = document.getElementById('lightbox');
        const lightboxContentEl = document.querySelector('.lightbox-content');
        const lightboxImgEl = document.getElementById('lightbox-img');
        const lightboxArtistEl = document.getElementById('lightbox-artist');
        const lightboxModelEl = document.getElementById('lightbox-model');
        const lightboxSeedEl = document.getElementById('lightbox-seed');
        const lightboxRelatedImagesContainer = document.getElementById('lightbox-related-images');
        const favoriteTextEl = document.getElementById('favorite-text');
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
        
        if (templateTextEl && typeof galleryData !== 'undefined' && galleryData.template) {
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
            modelSelectorEl.innerHTML = '';
            const allBtn = document.createElement('button');
            allBtn.className = 'model-button';
            allBtn.setAttribute('data-model', 'all');
            allBtn.textContent = 'All Models';
            allBtn.addEventListener('click', function() { filterByModel('all'); setActiveButton(this); });
            modelSelectorEl.appendChild(allBtn);
            
            [...allModels].sort().forEach(model => {
                const btn = document.createElement('button');
                btn.className = 'model-button';
                btn.setAttribute('data-model', model);
                btn.textContent = modelNameMap[model];
                btn.addEventListener('click', function() { filterByModel(model); setActiveButton(this); });
                modelSelectorEl.appendChild(btn);
            });

            const defaultModelId = 'nai-diffusion-4-5-full';
            let defaultModelButton = modelSelectorEl.querySelector(`button[data-model="${defaultModelId}"]`);
            if (defaultModelButton) setActiveButton(defaultModelButton);
            else if (allBtn) setActiveButton(allBtn);
        }
        
        function setActiveButton(btn) {
            if (!modelSelectorEl || !btn) return;
            modelSelectorEl.querySelectorAll('.model-button').forEach(el => el.classList.remove('active'));
            btn.classList.add('active');
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
            const imageIdStr = imageId.toString();
            const isNowFavorite = !favorites.has(imageIdStr);
            if (isNowFavorite) favorites.add(imageIdStr); else favorites.delete(imageIdStr);
            localStorage.setItem(FAVORITES_KEY, JSON.stringify([...favorites]));
            const cardIcon = galleryEl.querySelector(`.image-card[data-id="${imageIdStr}"] .favorite-icon-card`);
            if (cardIcon) cardIcon.classList.toggle('favorited', isNowFavorite);
            if (currentLightboxImage && currentLightboxImage.id === imageId) updateFavoriteButtonUI(isNowFavorite);
            if (showingFavorites && !isNowFavorite) filterGallery();
        }
        
        function updateFavoriteButtonUI(isFavorite) { 
            if (favoriteButtonEl && favoriteTextEl) {
                favoriteButtonEl.classList.toggle('favorited', isFavorite); 
                favoriteTextEl.textContent = isFavorite ? 'Remove from Favorites' : 'Add to Favorites';
            }
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
            searchBoxEl.addEventListener('input', function() {
                currentSearchTerm = this.value.toLowerCase().trim();
                clearTimeout(searchBoxEl.searchTimeout);
                searchBoxEl.searchTimeout = setTimeout(() => { filterGallery(); }, 300);
            });
        }
        
        function filterGallery() {
            const currentModel = modelSelectorEl ? (modelSelectorEl.querySelector('.model-button.active')?.getAttribute('data-model') || 'all') : 'all';
            filterByModel(currentModel);
        }
        
        function filterByModel(model) {
            if (!galleryEl) return;
            galleryEl.innerHTML = '';
            loadedImagesCount = 0;
            
            let filteredImages = (model === 'all') ? [...galleryData.sectionImages] : [...(imagesByModel[model] || [])];
            if (showingFavorites) {
                filteredImages = filteredImages.filter(img => favorites.has(img.id.toString()));
            }
            if (currentSearchTerm) {
                filteredImages = filteredImages.filter(img => {
                    const term = currentSearchTerm;
                    return (img.artist && img.artist.toLowerCase().includes(term)) ||
                           (img.prompt && img.prompt.toLowerCase().includes(term)) ||
                           ('character1' in img && img.character1.toLowerCase().includes(term)) ||
                           ('character2' in img && img.character2.toLowerCase().includes(term));
                });
            }
            
            shuffledImages = filteredImages.sort(() => Math.random() - 0.5);
            loadImages(24);
            if (loadingEl) loadingEl.style.display = shuffledImages.length > loadedImagesCount ? 'block' : 'none';
        }
        
        let shuffledImages = [];
        let loadedImagesCount = 0;
        let currentLightboxImage = null;
        
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
                card.setAttribute('data-id', img.id);
                const imgContainer = document.createElement('div');
                imgContainer.className = 'image-container';
                const favIconOnCard = document.createElement('div'); 
                favIconOnCard.className = 'favorite-icon-card';
                if (favorites.has(img.id.toString())) favIconOnCard.classList.add('favorited');
                favIconOnCard.addEventListener('click', (e) => { e.stopPropagation(); toggleFavorite(img.id); });
                imgContainer.appendChild(favIconOnCard);
                const imgEl = document.createElement('img');
                imgEl.src = THUMB_PATH + img.id + ".jpg";
                imgEl.alt = "Gallery image thumbnail";
                imgEl.loading = 'lazy';
                imgEl.style.width = GALLERY_IMAGE_THUMB_SCALE_PERCENT + '%';
                imgEl.style.height = 'auto';
                imgContainer.appendChild(imgEl);
                card.appendChild(imgContainer);
                card.addEventListener('click', () => { openLightbox(img); });
                fragment.appendChild(card);
            }
            if (galleryEl) galleryEl.appendChild(fragment);
            loadedImagesCount = endIndex;
            if (loadingEl) loadingEl.style.display = loadedImagesCount < shuffledImages.length ? 'block' : 'none';
        }
        
        function openLightbox(img) {
            currentLightboxImage = img;
            if (lightboxContentEl) lightboxContentEl.scrollTop = 0;
            lightboxImgEl.src = FULL_PATH + img.id + ".jpg";
            
            lightboxPromptArea.innerHTML = ''; // Clear previous content

            const createPromptBlock = (title, text, isCombined = false) => {
                const container = document.createElement('div');
                container.className = 'prompt-container';
                if (isCombined) container.style.borderTop = "2px solid var(--button-border)";
                if (isCombined) container.style.paddingTop = "1rem";
                
                const h4 = document.createElement('h4');
                h4.textContent = title;
                container.appendChild(h4);

                const pre = document.createElement('pre');
                pre.textContent = text;
                container.appendChild(pre);

                const button = document.createElement('button');
                button.className = 'copy-button';
                button.textContent = `Copy ${title}`;
                button.addEventListener('click', () => {
                    navigator.clipboard.writeText(text).then(() => showToast(`${title} copied!`));
                });
                container.appendChild(button);
                return container;
            };

            // --- CORRECTED LOGIC ---
            // Use the 'in' operator to check for property existence, not truthiness.
            // This is the robust way to handle this in JavaScript.
            if ('character1' in img && 'character2' in img) {
                // New Format (noncon.html)
                const combinedPrompt = `by ${img.artist}, very aesthetic, masterpiece, absurdres, no text, ${img.prompt}, ${img.character1}, ${img.character2}`;
                
                lightboxPromptArea.appendChild(createPromptBlock('Full Combined Prompt', combinedPrompt, false));
                lightboxPromptArea.appendChild(createPromptBlock('Scene Prompt', img.prompt, true));
                lightboxPromptArea.appendChild(createPromptBlock('Character 1', img.character1, false));
                lightboxPromptArea.appendChild(createPromptBlock('Character 2', img.character2, false));

            } else {
                // Old Format (backward compatibility)
                const tagsContainer = document.createElement('div');
                tagsContainer.className = 'tags-container-modal';
                const tags = img.prompt.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0);
                tags.forEach(tag => {
                    const tagSpan = document.createElement('span');
                    tagSpan.className = 'clickable-tag-modal';
                    tagSpan.textContent = tag;
                    tagSpan.title = `Search for "${tag}"`;
                    tagSpan.addEventListener('click', () => {
                        if (searchBoxEl) {
                            searchBoxEl.value = tag;
                            searchBoxEl.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                        closeLightbox();
                    });
                    tagsContainer.appendChild(tagSpan);
                    tagsContainer.appendChild(document.createTextNode(' '));
                });
                lightboxPromptArea.appendChild(tagsContainer);
                lightboxPromptArea.appendChild(createPromptBlock('Prompt', img.prompt, false));
            }

            // The rest of the function remains the same...
            if (lightboxArtistEl) lightboxArtistEl.textContent = img.artist;
            if (lightboxModelEl) lightboxModelEl.textContent = img.modelName;
            if (lightboxSeedEl) lightboxSeedEl.textContent = img.seed;
            updateFavoriteButtonUI(favorites.has(img.id.toString()));
            if (lightboxArtistEl) {
                lightboxArtistEl.onclick = () => { if (img.artist) { navigator.clipboard.writeText(img.artist).then(() => showToast(`Copied artist: ${img.artist}`)).catch(err => console.error('Failed to copy artist:', err)); } };
            }
            if (lightboxRelatedImagesContainer) {
                lightboxRelatedImagesContainer.innerHTML = '';
                const relatedImages = galleryData.sectionImages.filter(relImg => relImg.id !== img.id && relImg.artist === img.artist && relImg.model === img.model).slice(0, 20); 
                if (relatedImages.length > 0) {
                    const relatedTitle = document.createElement('h4');
                    relatedTitle.textContent = 'More from this artist & model:';
                    lightboxRelatedImagesContainer.appendChild(relatedTitle);
                    const relatedGrid = document.createElement('div');
                    relatedGrid.className = 'related-images-grid';
                    relatedImages.forEach(relImg => {
                        const relImgEl = document.createElement('img');
                        relImgEl.src = THUMB_PATH + relImg.id + ".jpg";
                        relImgEl.alt = "Related image thumbnail";
                        relImgEl.className = 'related-image';
                        if (favorites.has(relImg.id.toString())) relImgEl.classList.add('favorited');
                        relImgEl.addEventListener('click', (e) => { e.stopPropagation(); openLightbox(relImg); });
                        relatedGrid.appendChild(relImgEl);
                    });
                    lightboxRelatedImagesContainer.appendChild(relatedGrid);
                }
            }
            if (lightboxEl) lightboxEl.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        
        function closeLightbox() {
            if (lightboxEl) lightboxEl.classList.remove('active');
            if (lightboxImgEl) lightboxImgEl.src = '';
            currentLightboxImage = null;
            document.body.style.overflow = '';
        }
        
        if (favoriteButtonEl) favoriteButtonEl.addEventListener('click', () => { if (currentLightboxImage) toggleFavorite(currentLightboxImage.id); });
        if (lightboxImgEl && fullscreenOverlay && fullscreenImg) {
            lightboxImgEl.addEventListener('click', () => { fullscreenImg.src = lightboxImgEl.src; fullscreenOverlay.classList.add('visible'); });
        }
        if (fullscreenOverlay) fullscreenOverlay.addEventListener('click', () => { fullscreenOverlay.classList.remove('visible'); fullscreenImg.src = ''; });
        if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
        if (lightboxEl) lightboxEl.addEventListener('click', (e) => { if (e.target === lightboxEl) closeLightbox(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && lightboxEl && lightboxEl.classList.contains('active')) closeLightbox(); });
        window.addEventListener('scroll', () => {
            if (!loadingEl || loadingEl.style.display === 'none') return; 
            if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 500) { if (loadedImagesCount < shuffledImages.length) loadImages(12); }
        });
        
        filterGallery();
    }

    function mainInit() {
        if (typeof galleryData === 'undefined' || !galleryData.sectionImages) {
            console.error("galleryData is not defined. Cannot initialize gallery.");
            return;
        }
        const isNsfw = galleryData.isNsfwSection || false;
        const disclaimerAccepted = localStorage.getItem(AGE_DISCLAIMER_KEY) === 'true';
        if (isNsfw && !disclaimerAccepted) showAgeDisclaimer(); else initializeGallery();
    }

    mainInit();
});
