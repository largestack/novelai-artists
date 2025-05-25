/**
 * Character Gallery JS - For NovelAI Character Galleries
 */

const GALLERY_IMAGE_THUMB_SCALE_PERCENT = 100; // Target image width as % of its original width. Adjust as needed.
const THUMB_PATH = "https://f005.backblazeb2.com/file/novelai-images/thumb/"; // Path to thumbnail images
const FULL_PATH = "https://f005.backblazeb2.com/file/novelai-images/full/"; // Path to full images
const AGE_DISCLAIMER_KEY = 'ageDisclaimerAccepted_v1'; // Added _v1 in case structure changes later

document.addEventListener('DOMContentLoaded', function() {

    function showAgeDisclaimer() {
        const overlay = document.getElementById('age-disclaimer-overlay');
        const confirmBtn = document.getElementById('age-confirm-button');
        const exitBtn = document.getElementById('age-exit-button');

        if (!overlay || !confirmBtn || !exitBtn) {
            console.error("Age disclaimer HTML elements not found. Gallery cannot initialize.");
            // Optionally, display a message to the user in the body
            document.body.innerHTML = "<p style='text-align:center; padding-top: 50px; font-size: 1.2em;'>Error: Age verification components are missing. Please contact support.</p>";
            return;
        }

        overlay.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent scrolling background

        confirmBtn.onclick = () => {
            localStorage.setItem(AGE_DISCLAIMER_KEY, 'true');
            overlay.style.display = 'none';
            document.body.style.overflow = '';
            initializeGallery();
        };

        exitBtn.onclick = () => {
            const modalContent = document.getElementById('age-disclaimer-modal');
            if (modalContent) {
                modalContent.innerHTML = '<h2>Access Denied</h2><p>You must be 18 or older to view this content. You can close this window or tab.</p>';
            }
            // Prevent gallery initialization
        };
    }

    function initializeGallery() {
        // Elements
        const galleryEl = document.getElementById('gallery');
        const lightboxEl = document.getElementById('lightbox');
        const lightboxImgEl = document.getElementById('lightbox-img');
        // const lightboxCharacterNameEl = document.getElementById('lightbox-character-name'); // Removed as per request
        const lightboxTagsContainerEl = document.getElementById('lightbox-tags-container');
        const lightboxArtistEl = document.getElementById('lightbox-artist');
        const lightboxModelEl = document.getElementById('lightbox-model');
        const lightboxPromptEl = document.getElementById('lightbox-prompt');
        const lightboxSeedEl = document.getElementById('lightbox-seed');
        const lightboxRelatedImagesContainer = document.getElementById('lightbox-related-images');
        const favoriteIconEl = document.getElementById('favorite-icon-gfx'); // Corrected ID if you meant the visual icon
        const favoriteTextEl = document.getElementById('favorite-text');
        const favoriteButtonEl = document.getElementById('favorite-button');
        const favoritesToggleBtn = document.getElementById('favorites-toggle');
        const copyPromptBtn = document.getElementById('copy-prompt');
        const closeBtn = document.querySelector('.lightbox .close');
        const templateTextEl = document.getElementById('template-text');
        const modelSelectorEl = document.getElementById('model-selector');
        const loadingEl = document.getElementById('loading');
        const searchBoxEl = document.getElementById('search-box');

        if (!galleryEl || !lightboxEl || !modelSelectorEl) {
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
            if (!imagesByModel[img.model]) {
                imagesByModel[img.model] = [];
            }
            imagesByModel[img.model].push(img);
            allModels.add(img.model);
    
            // modelName is now expected to be provided by galleryData directly from Python
            if (img.modelName) {
                modelNameMap[img.model] = img.modelName;
            } else {
                // Fallback if modelName is somehow missing
                modelNameMap[img.model] = img.model;
            }
        });

        if (modelSelectorEl) {
            modelSelectorEl.innerHTML = ''; // Clear any existing buttons
            const allBtn = document.createElement('button');
            allBtn.className = 'model-button'; // Default to not active
            allBtn.setAttribute('data-model', 'all');
            allBtn.textContent = 'All Models';
            allBtn.addEventListener('click', function() {
                filterByModel('all');
                setActiveButton(this);
            });
            modelSelectorEl.appendChild(allBtn);
            
            [...allModels].sort().forEach(model => {
                const modelName = modelNameMap[model] || model;
                const btn = document.createElement('button');
                btn.className = 'model-button';
                btn.setAttribute('data-model', model);
                btn.textContent = modelName;
                btn.addEventListener('click', function() {
                    filterByModel(model);
                    setActiveButton(this);
                });
                modelSelectorEl.appendChild(btn);
            });

            // Set default model
            const defaultModelId = 'nai-diffusion-4-full';
            let defaultModelButton = modelSelectorEl.querySelector(`button[data-model="${defaultModelId}"]`);
            
            if (defaultModelButton) {
                setActiveButton(defaultModelButton); // This will also remove 'active' from others
            } else if (allBtn) {
                setActiveButton(allBtn); // Fallback to 'All Models' if default isn't found
            }
        }
        
        function setActiveButton(btn) {
            if (!modelSelectorEl || !btn) return;
            modelSelectorEl.querySelectorAll('.model-button').forEach(el => {
                el.classList.remove('active');
            });
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
            setTimeout(() => {
                toast.classList.remove('visible');
            }, 2000);
        }
        
        function toggleFavorite(imageId) {
            const imageIdStr = imageId.toString();
            if (favorites.has(imageIdStr)) {
                favorites.delete(imageIdStr);
                updateFavoriteButtonUI(false);
            } else {
                favorites.add(imageIdStr);
                updateFavoriteButtonUI(true);
            }
            localStorage.setItem(FAVORITES_KEY, JSON.stringify([...favorites]));
            if (showingFavorites) {
                filterGallery(); 
            }
        }
        
        function updateFavoriteButtonUI(isFavorite) { 
            if (favoriteButtonEl && favoriteTextEl) { // favoriteIconEl might be the visual icon itself
                favoriteButtonEl.classList.toggle('favorited', isFavorite); 
                favoriteTextEl.textContent = isFavorite ? 'Remove from Favorites' : 'Add to Favorites';
            }
        }
        
        if (favoritesToggleBtn) {
            favoritesToggleBtn.addEventListener('click', function() {
                showingFavorites = !showingFavorites;
                this.textContent = showingFavorites ? 'Show All' : 'Show Favorites Only';
                this.classList.toggle('active-filter', showingFavorites);
                filterGallery();
            });
        }

        if (searchBoxEl) {
            searchBoxEl.addEventListener('input', function() {
                currentSearchTerm = this.value.toLowerCase().trim();
                clearTimeout(searchBoxEl.searchTimeout);
                searchBoxEl.searchTimeout = setTimeout(() => {
                    filterGallery();
                }, 300);
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
            
            let filteredImages = [];
            if (model === 'all') {
                filteredImages = [...galleryData.sectionImages];
            } else {
                filteredImages = [...(imagesByModel[model] || [])];
            }
            
            if (showingFavorites) {
                filteredImages = filteredImages.filter(img => favorites.has(img.id.toString()));
            }

            if (currentSearchTerm) {
                filteredImages = filteredImages.filter(img => {
                    const artistMatch = img.artist && img.artist.toLowerCase().includes(currentSearchTerm);
                    const tagsMatch = img.prompt && img.prompt.toLowerCase().includes(currentSearchTerm); 
                    return artistMatch || tagsMatch;
                });
            }
            
            shuffledImages = filteredImages.sort(() => Math.random() - 0.5);
            
            loadImages(24); // Initial load
            if (loadingEl) loadingEl.style.display = shuffledImages.length > loadedImagesCount ? 'block' : 'none';
        }
        
        let shuffledImages = []; // Will be populated by filterByModel
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
                // Data attributes for artist/model not strictly needed on card if not shown, but can be kept for debugging
                card.setAttribute('data-model', img.model || '');
                card.setAttribute('data-artist', img.artist || '');
                
                const imgContainer = document.createElement('div');
                imgContainer.className = 'image-container';
                
                const favIconOnCard = document.createElement('div'); 
                favIconOnCard.className = 'favorite-icon-card'; // Use a distinct class for card icon if styling differs
                if (favorites.has(img.id.toString())) {
                    favIconOnCard.classList.add('favorited');
                }
                favIconOnCard.addEventListener('click', function(e) {
                    e.stopPropagation(); // Prevent card click (opening lightbox)
                    toggleFavorite(img.id); 
                    // Update visual state of this icon on the card
                    favIconOnCard.classList.toggle('favorited', favorites.has(img.id.toString()));
                    // If filter shows only favorites, and this is un-favorited, it might disappear.
                    // This is handled by filterGallery if showingFavorites is true.
                });
                imgContainer.appendChild(favIconOnCard);
                
                const imgEl = document.createElement('img');
                imgEl.src = THUMB_PATH + img.id + ".jpg";
                imgEl.alt = "Gallery image thumbnail"; // Alt text should be descriptive but prompt is too long here
                imgEl.loading = 'lazy';
                imgEl.style.width = GALLERY_IMAGE_THUMB_SCALE_PERCENT + '%';
                imgEl.style.height = 'auto';
                imgContainer.appendChild(imgEl);
                
                card.appendChild(imgContainer);
                // REMOVED: image-card-info (prompt, artist, model) from card display
                
                card.addEventListener('click', function() {
                    openLightbox(img);
                });
                
                fragment.appendChild(card);
            }
            
            if (galleryEl) galleryEl.appendChild(fragment);
            loadedImagesCount = endIndex;
            if (loadingEl) loadingEl.style.display = loadedImagesCount < shuffledImages.length ? 'block' : 'none';
        }
        
        function openLightbox(img) {
            currentLightboxImage = img;
            
            lightboxImgEl.src = FULL_PATH + img.id + ".jpg";
            
            // REMOVED: lightboxCharacterNameEl.textContent = img.prompt; (title with full prompt)

            if (lightboxTagsContainerEl) {
                lightboxTagsContainerEl.innerHTML = ''; 
                const tags = img.prompt.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0);
                
                tags.forEach(tag => {
                    const tagSpan = document.createElement('span');
                    tagSpan.className = 'clickable-tag-modal';
                    tagSpan.textContent = tag;
                    tagSpan.title = `Search for "${tag}"`;
                    tagSpan.addEventListener('click', () => {
                        if (searchBoxEl) {
                            searchBoxEl.value = tag;
                            searchBoxEl.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
                        }
                        closeLightbox();
                    });
                    lightboxTagsContainerEl.appendChild(tagSpan);
                    lightboxTagsContainerEl.appendChild(document.createTextNode(' ')); 
                });
            }

            if (lightboxArtistEl) lightboxArtistEl.textContent = img.artist;
            if (lightboxModelEl) lightboxModelEl.textContent = img.modelName || img.model; // Use modelName from data
            if (lightboxPromptEl) lightboxPromptEl.textContent = img.prompt;
            if (lightboxSeedEl) lightboxSeedEl.textContent = img.seed;
            
            updateFavoriteButtonUI(favorites.has(img.id.toString()));

            if (lightboxArtistEl) {
                lightboxArtistEl.onclick = null; 
                lightboxArtistEl.onclick = () => {
                    if (img.artist) {
                        navigator.clipboard.writeText(img.artist).then(() => {
                            showToast(`Copied artist: ${img.artist}`);
                        }).catch(err => {
                            console.error('Failed to copy artist:', err);
                            showToast('Failed to copy artist');
                        });
                    }
                };
            }
            
            if (lightboxRelatedImagesContainer) {
                lightboxRelatedImagesContainer.innerHTML = '';
                const relatedImages = galleryData.sectionImages.filter(
                    relatedImg => relatedImg.id !== img.id && 
                                  relatedImg.artist === img.artist && 
                                  relatedImg.model === img.model
                ).slice(0, 20); 
                
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
                        relImgEl.setAttribute('data-id', relImg.id);
                        if (favorites.has(relImg.id.toString())) {
                            relImgEl.classList.add('favorited');
                        }
                        relImgEl.addEventListener('click', function(e) {
                            e.stopPropagation();
                            openLightbox(relImg);
                        });
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
            if (lightboxTagsContainerEl) {
                lightboxTagsContainerEl.innerHTML = '';
            }
            if (lightboxRelatedImagesContainer) {
                lightboxRelatedImagesContainer.innerHTML = '';
            }
            document.body.style.overflow = '';
        }
        
        if (favoriteButtonEl) { 
            favoriteButtonEl.addEventListener('click', function() {
                if (currentLightboxImage) {
                    toggleFavorite(currentLightboxImage.id);
                    
                    // Update heart icon on the card in the main gallery if it's visible
                    const cardInGallery = galleryEl.querySelector(`.image-card[data-id="${currentLightboxImage.id}"]`);
                    if (cardInGallery) {
                        const favIconOnCard = cardInGallery.querySelector('.favorite-icon-card');
                        if (favIconOnCard) {
                            favIconOnCard.classList.toggle('favorited', favorites.has(currentLightboxImage.id.toString()));
                        }
                    }
                }
            });
        }
        
        if (copyPromptBtn && lightboxPromptEl) {
            copyPromptBtn.addEventListener('click', function() {
                navigator.clipboard.writeText(lightboxPromptEl.textContent)
                    .then(() => showToast("Prompt copied!"))
                    .catch(err => console.error('Failed to copy prompt:', err));
            });
        }
        
        if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
        if (lightboxEl) {
            lightboxEl.addEventListener('click', function(e) {
                if (e.target === lightboxEl) {
                    closeLightbox();
                }
            });
        }
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && lightboxEl && lightboxEl.classList.contains('active')) {
                closeLightbox();
            }
        });
        
        window.addEventListener('scroll', function() {
            if (!loadingEl || loadingEl.style.display === 'none') return; 
            const scrollPosition = window.scrollY + window.innerHeight;
            const pageHeight = document.documentElement.scrollHeight;
            
            if (pageHeight - scrollPosition < 500) { // Load more when 500px from bottom
                if (loadedImagesCount < shuffledImages.length) {
                    // Debounce or throttle this if it fires too rapidly
                    setTimeout(() => loadImages(12), 200); // Load fewer images more frequently if needed
                }
            }
        });
        
        // Initial gallery population
        filterGallery(); 
    } // End of initializeGallery

    // Age Disclaimer Check
    if (typeof galleryData !== 'undefined' && galleryData.sectionImages) { // Ensure galleryData is loaded
        if (localStorage.getItem(AGE_DISCLAIMER_KEY) !== 'true') {
            showAgeDisclaimer();
        } else {
            initializeGallery();
        }
    } else {
        // Handle case where galleryData might not be defined (e.g. if script loaded before data)
        // This can happen if galleryData script block is after this script file.
        // For this setup, galleryData is expected to be defined.
        console.warn("galleryData is not defined. Age disclaimer and gallery initialization might be affected.");
        // Fallback or error message if galleryData is critical for disclaimer logic as well.
        // For now, assume galleryData is primarily for the gallery itself.
        // The disclaimer HTML should exist independently.
         if (localStorage.getItem(AGE_DISCLAIMER_KEY) !== 'true') {
            showAgeDisclaimer(); // Show disclaimer even if gallery data is not ready.
        } else {
            // If accepted, but gallery data not ready, initializeGallery might fail or wait.
            // This implies initializeGallery should also check for galleryData.
            // The current initializeGallery already expects galleryData.
            initializeGallery();
        }
    }

});
