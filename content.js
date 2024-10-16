async function analyzeContent(contentText) {
    const formData = new FormData();
    formData.append('text', contentText);

    try {
        const response = await fetch('http://localhost:5000/analyze_content', {
            method: 'POST',
            body: formData
        });

        console.log('Response:', response); // cette ligne pour voir la réponse

        if (!response.ok) {
            const errorText = await response.text(); // Lire le texte de l'erreur
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const result = await response.json();
        return result.isTextInappropriate; // Renvoie vrai si le texte est inapproprié
    } catch (error) {
        console.error('Erreur lors de l\'analyse du contenu :', error);
        return false;
    }
}

async function filterTweets() {
    const tweetArticles = document.querySelectorAll('article');

    for (const tweetArticle of tweetArticles) {
        const tweetTextElement = tweetArticle.querySelector('div[data-testid="tweetText"] > span');
        const textContent = tweetTextElement ? tweetTextElement.innerText : '';
        console.log('Text content:', textContent); // Log du contenu du tweet pour le débog

        // Analyser uniquement le texte
        const isInappropriate = await analyzeContent(textContent);
        
        if (isInappropriate) {
            //tweetArticle.style.element.display = 'none';
            tweetArticle.style.filter = 'blur(100px)';
            console.log("Tweet masqué en raison de contenu inapproprié.");
        } else {
            console.log("Tweet non masqué");
        }
    }
}

// Observer les changements dans le DOM (tweets chargés dynamiquement)
const observer = new MutationObserver(filterTweets);
observer.observe(document.body, { childList: true, subtree: true });

// Filtrer les tweets lors du chargement initial
filterTweets();
