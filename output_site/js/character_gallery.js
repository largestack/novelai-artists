/**
 * Character Gallery JS - For NovelAI Character Galleries
 */

const GALLERY_IMAGE_THUMB_SCALE_PERCENT = 100; // Target image width as % of its original width. Adjust as needed.
const THUMB_PATH = "./images/thumb/"; // Path to thumbnail images
const FULL_PATH = "./images/full/"; // Path to full images

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const galleryEl = document.getElementById('gallery');
    const lightboxEl = document.getElementById('lightbox');
    const lightboxImgEl = document.getElementById('lightbox-img');
    // Updated lightbox character elements
    const lightboxCharacterNameEl = document.getElementById('lightbox-character-name');
    const lightboxTagsContainerEl = document.getElementById('lightbox-tags-container');
    const lightboxArtistEl = document.getElementById('lightbox-artist');
    const lightboxModelEl = document.getElementById('lightbox-model');
    const lightboxPromptEl = document.getElementById('lightbox-prompt');
    const lightboxSeedEl = document.getElementById('lightbox-seed');
    const lightboxRelatedImagesContainer = document.getElementById('lightbox-related-images');
    const favoriteIconEl = document.getElementById('favorite-icon'); 
    const favoriteTextEl = document.getElementById('favorite-text'); 
    const favoriteButtonEl = document.getElementById('favorite-button'); 
    const favoritesToggleBtn = document.getElementById('favorites-toggle'); 
    const copyPromptBtn = document.getElementById('copy-prompt');
    const closeBtn = document.querySelector('.lightbox .close');
    const templateTextEl = document.getElementById('template-text');
    const modelSelectorEl = document.getElementById('model-selector'); 
    const loadingEl = document.getElementById('loading');
    const searchBoxEl = document.getElementById('search-box');
    
    // Set template text
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
        if (!imagesByModel[img.model]) {
            imagesByModel[img.model] = [];
        }
        imagesByModel[img.model].push(img);
        allModels.add(img.model);

        if (img.model == 'nai-diffusion-4-full')
            img.modelName = 'NAI Diffusion 4 Full';
        else if (img.model == 'nAI-diffusion-4-curated-preview')
            img.modelName = 'NAI Diffusion 4 Curated Preview';
        else if (img.model == 'nai-diffusion-4-5-curated')
            img.modelName = 'NAI Diffusion 4.5 Curated';
        
        if (img.modelName) {
            modelNameMap[img.model] = img.modelName;
        }
    });

    if (modelSelectorEl) {
        const allBtn = document.createElement('button');
        allBtn.className = 'model-button active';
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
    }
    
    function setActiveButton(btn) {
        if (!modelSelectorEl) return;
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
        if (favoriteIconEl && favoriteTextEl) { 
            favoriteButtonEl.classList.toggle('favorited', isFavorite); 
            favoriteTextEl.textContent = isFavorite ? 'Remove from Favorites' : 'Add to Favorites';
        }
    }
    
    if (favoritesToggleBtn) {
        favoritesToggleBtn.addEventListener('click', function() {
            showingFavorites = !showingFavorites;
            this.textContent = showingFavorites ? 'Show All' : 'Show Favorites';
            filterGallery();
        });
    }

    if (searchBoxEl) {
        searchBoxEl.addEventListener('input', function() {
            currentSearchTerm = this.value.toLowerCase().trim();
            // Debounce filterGallery call for better performance on rapid typing
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
                const artistMatch = img.artist.toLowerCase().includes(currentSearchTerm);
                const tagsMatch = img.prompt.toLowerCase().includes(currentSearchTerm); 
                return artistMatch || tagsMatch;
            });
        }
        
        shuffledImages = filteredImages.sort(() => Math.random() - 0.5);
        
        loadImages(24);
        loadingEl.style.display = shuffledImages.length > loadedImagesCount ? 'block' : 'none';
    }
    
    let shuffledImages = [...galleryData.sectionImages].sort(() => Math.random() - 0.5);
    let loadedImagesCount = 0;
    let currentLightboxImage = null;
    
    function addPromptHoverEffects() {
        const promptElements = document.querySelectorAll('.image-card .prompt-preview');
        promptElements.forEach(el => {
            const fullPrompt = el.getAttribute('data-full-prompt');
            el.title = fullPrompt;
        });
    }
    
    function loadImages(count) {
        if (loadedImagesCount >= shuffledImages.length) {
            loadingEl.style.display = 'none';
            return;
        }
        
        const fragment = document.createDocumentFragment();
        const endIndex = Math.min(loadedImagesCount + count, shuffledImages.length);
        
        for (let i = loadedImagesCount; i < endIndex; i++) {
            const img = shuffledImages[i];
            
            const card = document.createElement('div');
            card.className = 'image-card';
            card.setAttribute('data-id', img.id);
            card.setAttribute('data-model', img.model || '');
            card.setAttribute('data-artist', img.artist || '');
            
            if (favorites.has(img.id.toString())) {
                card.classList.add('favorited');
            }
            
            const imgContainer = document.createElement('div');
            imgContainer.className = 'image-container';
            
            const favIconOnCard = document.createElement('div'); 
            favIconOnCard.className = 'favorite-icon'; 
            if (favorites.has(img.id.toString())) {
                favIconOnCard.classList.add('favorited');
            }
            favIconOnCard.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleFavorite(img.id); 
                card.classList.toggle('favorited', favorites.has(img.id.toString())); 
                favIconOnCard.classList.toggle('favorited', favorites.has(img.id.toString())); 
            });
            imgContainer.appendChild(favIconOnCard);
            
            const imgEl = document.createElement('img');
            imgEl.src = THUMB_PATH + img.id + ".jpg"; // Use the thumbnail path
            imgEl.alt = img.prompt;
            imgEl.loading = 'lazy';
            // Set width as % of original image size using the constant
            imgEl.style.width = GALLERY_IMAGE_THUMB_SCALE_PERCENT + '%'; // MODIFIED LINE
            imgEl.style.height = 'auto'; // Maintain aspect ratio
            imgContainer.appendChild(imgEl);
            
            const infoEl = document.createElement('div');
            infoEl.className = 'image-card-info';
            
            const nameEl = document.createElement('h3');
            nameEl.textContent = truncateText(img.prompt, 30);
            nameEl.title = img.prompt;
            infoEl.appendChild(nameEl);
            
            const artistModelEl = document.createElement('div');
            artistModelEl.className = 'artist-model-info';
            artistModelEl.innerHTML = `<span>by ${img.artist}</span> • <span>${img.modelName || img.model}</span>`;
            infoEl.appendChild(artistModelEl);
            
            const promptPreview = document.createElement('div');
            promptPreview.className = 'prompt-preview';
            promptPreview.textContent = truncatePrompt(img.prompt, 60);
            promptPreview.setAttribute('data-full-prompt', img.prompt);
            infoEl.appendChild(promptPreview);
            
            promptPreview.addEventListener('click', function(e) {
                e.stopPropagation(); 
                navigator.clipboard.writeText(img.prompt)
                    .then(() => showToast("Prompt copied!"))
                    .catch(err => console.error('Failed to copy prompt:', err));
            });
            
            card.appendChild(imgContainer);
            card.appendChild(infoEl);
            
            card.addEventListener('click', function() {
                openLightbox(img);
            });
            
            fragment.appendChild(card);
        }
        
        galleryEl.appendChild(fragment);
        loadedImagesCount = endIndex;
        addPromptHoverEffects();
        loadingEl.style.display = loadedImagesCount < shuffledImages.length ? 'block' : 'none';
    }
    
    function truncateText(text, maxLength) {
        if (!text || typeof text !== 'string') return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    function truncatePrompt(text, maxLength) {
        if (!text || typeof text !== 'string') return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    function openLightbox(img) {
        currentLightboxImage = img;
        
        lightboxImgEl.src = FULL_PATH + img.id + ".jpg"; // Use the full image path
        //lightboxImgEl.src = img.full;
        
        // Display full character description in the designated H3
        if (lightboxCharacterNameEl) {
            lightboxCharacterNameEl.textContent = img.prompt;
        }

        // Clear previous tags and generate new clickable tags
        if (lightboxTagsContainerEl) {
            lightboxTagsContainerEl.innerHTML = ''; // Clear previous tags
            const tags = img.prompt.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0);
            
            tags.forEach(tag => {
                const tagSpan = document.createElement('span');
                tagSpan.className = 'clickable-tag-modal';
                tagSpan.textContent = tag;
                tagSpan.title = `Search for "${tag}"`;
                tagSpan.addEventListener('click', () => {
                    if (searchBoxEl) {
                        searchBoxEl.value = tag;
                        // Dispatch 'input' event to trigger search logic
                        searchBoxEl.dispatchEvent(new Event('input', { bubbles: true, cancelable: true }));
                    }
                    closeLightbox();
                });
                lightboxTagsContainerEl.appendChild(tagSpan);
                lightboxTagsContainerEl.appendChild(document.createTextNode(' ')); // Add space between tags
            });
        }

        lightboxArtistEl.textContent = img.artist;
        lightboxModelEl.textContent = img.modelName || img.model;
        lightboxPromptEl.textContent = img.prompt;
        lightboxSeedEl.textContent = img.seed;
        
        updateFavoriteButtonUI(favorites.has(img.id.toString()));

        lightboxArtistEl.onclick = null; 
        lightboxArtistEl.onclick = () => {
            navigator.clipboard.writeText(img.artist).then(() => {
                showToast(`Copied artist: ${img.artist}`);
            }).catch(err => {
                console.error('Failed to copy artist:', err);
                showToast('Failed to copy artist');
            });
        };
        
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
                    relImgEl.src = THUMB_PATH + relImg.id + ".jpg"; // Use the thumbnail path
                    //relImgEl.src = relImg.thumb;
                    relImgEl.alt = relImg.prompt;
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
        
        lightboxEl.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    function closeLightbox() {
        lightboxEl.classList.remove('active');
        lightboxImgEl.src = '';
        currentLightboxImage = null;
        if (lightboxTagsContainerEl) {
            lightboxTagsContainerEl.innerHTML = ''; // Clear tags on close
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
                
                const cardInGallery = galleryEl.querySelector(`.image-card[data-id="${currentLightboxImage.id}"]`);
                if (cardInGallery) {
                    const favIconOnCard = cardInGallery.querySelector('.favorite-icon');
                    cardInGallery.classList.toggle('favorited', favorites.has(currentLightboxImage.id.toString()));
                    if (favIconOnCard) {
                        favIconOnCard.classList.toggle('favorited', favorites.has(currentLightboxImage.id.toString()));
                    }
                }
            }
        });
    }
    
    if (copyPromptBtn) {
        copyPromptBtn.addEventListener('click', function() {
            navigator.clipboard.writeText(lightboxPromptEl.textContent)
                .then(() => showToast("Prompt copied!"))
                .catch(err => console.error('Failed to copy prompt:', err));
        });
    }
    
    closeBtn.addEventListener('click', closeLightbox);
    lightboxEl.addEventListener('click', function(e) {
        if (e.target === lightboxEl) {
            closeLightbox();
        }
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && lightboxEl.classList.contains('active')) {
            closeLightbox();
        }
    });
    
    window.addEventListener('scroll', function() {
        if (loadingEl.style.display === 'none') return; 
        const scrollPosition = window.scrollY + window.innerHeight;
        const pageHeight = document.documentElement.scrollHeight;
        
        if (pageHeight - scrollPosition < 500) {
            if (loadedImagesCount < shuffledImages.length) {
                setTimeout(() => loadImages(24), 300);
            }
        }
    });
    
    filterGallery(); 
});
