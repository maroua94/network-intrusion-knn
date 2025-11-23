// ===== CONFIGURATION =====
const API_URL = 'http://localhost:8000/predict';

// ===== ÉLÉMENTS DOM =====
const predictionForm = document.getElementById('predictionForm');
const predictBtn = document.getElementById('predictBtn');
const loader = document.getElementById('loader');
const resultContainer = document.getElementById('resultContainer');
const resultCard = document.getElementById('resultCard');
const resultIcon = document.getElementById('resultIcon');
const resultTitle = document.getElementById('resultTitle');
const resultMessage = document.getElementById('resultMessage');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');
const historyBody = document.getElementById('historyBody');
const historyTable = document.getElementById('historyTable');
const emptyState = document.getElementById('emptyState');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');

// ===== ÉTAT DE L'APPLICATION =====
let predictionHistory = [];

// ===== INITIALISATION =====
document.addEventListener('DOMContentLoaded', () => {
    loadHistoryFromStorage();
    updateHistoryDisplay();
    checkAPIConnection();
});

// ===== VÉRIFICATION DE LA CONNEXION API =====
async function checkAPIConnection() {
    try {
        const response = await fetch('http://localhost:8000/', {
            method: 'GET',
            mode: 'cors'
        });
        console.log('✅ API accessible');
    } catch (error) {
        console.warn('⚠️ API non accessible - Vérifiez que le serveur est démarré');
    }
}

// ===== GESTION DU FORMULAIRE =====
predictionForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Récupération des valeurs
    const nbPacketsInput = document.getElementById('nbPackets').value;
    const dureeConnexionInput = document.getElementById('dureeConnexion').value;
    
    // Conversion en nombres
    const nbPackets = parseFloat(nbPacketsInput);
    const dureeConnexion = parseFloat(dureeConnexionInput);
    
    // Validation
    if (isNaN(nbPackets) || isNaN(dureeConnexion)) {
        showError('Veuillez entrer des valeurs numériques valides');
        return;
    }
    
    if (nbPackets < 0 || dureeConnexion < 0) {
        showError('Les valeurs doivent être positives');
        return;
    }
    
    // Préparation de la requête (IMPORTANT: noms exacts du backend)
    const requestData = {
        nb_packets: nbPackets,
        duree_connexion: dureeConnexion
    };
    
    console.log('🔍 Données à envoyer:', requestData);
    
    // Appel de l'API
    await makePrediction(requestData);
});

// ===== APPEL API =====
async function makePrediction(data) {
    // Afficher le loader
    showLoader();
    hideResult();
    hideError();
    
    try {
        console.log('📤 Envoi de la requête:', data);
        console.log('📤 JSON stringifié:', JSON.stringify(data));
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        console.log('📥 Statut de la réponse:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Erreur HTTP ${response.status}: ${errorText}`);
        }
        
        const result = await response.json();
        console.log('✅ Résultat reçu:', result);
        
        // Traiter la réponse
        handlePredictionResult(result, data);
        
    } catch (error) {
        console.error('❌ Erreur lors de la prédiction:', error);
        
        // Messages d'erreur détaillés
        let errorMsg = '';
        
        if (error.message.includes('Failed to fetch') || error.name === 'TypeError') {
            errorMsg = `
                <strong>Erreur de connexion à l'API</strong><br>
                <small>
                • Vérifiez que le serveur backend est démarré sur http://localhost:8000<br>
                • Vérifiez que CORS est activé dans votre API (voir la documentation)<br>
                • Commande pour démarrer le serveur : <code>uvicorn main:app --reload</code>
                </small>
            `;
        } else if (error.message.includes('CORS')) {
            errorMsg = `
                <strong>Erreur CORS détectée</strong><br>
                <small>
                Votre backend doit autoriser les requêtes cross-origin.<br>
                Ajoutez CORSMiddleware dans votre API FastAPI (voir documentation).
                </small>
            `;
        } else {
            errorMsg = error.message;
        }
        
        showError(errorMsg);
    } finally {
        hideLoader();
    }
}

// ===== TRAITEMENT DU RÉSULTAT =====
function handlePredictionResult(result, inputData) {
    // Déterminer si c'est une attaque (gestion flexible des formats de réponse)
    let isAttack = false;
    
    if (result.prediction) {
        const pred = result.prediction.toString().toLowerCase();
        isAttack = pred === 'attaque' || pred === 'attack' || pred === '1';
    } else if (result.result) {
        const pred = result.result.toString().toLowerCase();
        isAttack = pred === 'attaque' || pred === 'attack' || pred === '1';
    }
    
    // Afficher le résultat
    displayResult(isAttack);
    
    // Ajouter à l'historique
    addToHistory({
        timestamp: new Date(),
        nbPackets: inputData.nb_packets,
        dureeConnexion: inputData.duree_connexion,
        prediction: isAttack ? 'Attaque' : 'Normal',
        isAttack: isAttack
    });
}

// ===== AFFICHAGE DU RÉSULTAT =====
function displayResult(isAttack) {
    // Retirer les classes précédentes
    resultCard.classList.remove('attack', 'normal');
    
    if (isAttack) {
        // Affichage attaque
        resultCard.classList.add('attack');
        resultIcon.textContent = '🚨';
        resultTitle.textContent = 'Attaque Détectée !';
        resultMessage.textContent = 'Une activité suspecte a été identifiée sur cette connexion. Action de sécurité recommandée.';
    } else {
        // Affichage normal
        resultCard.classList.add('normal');
        resultIcon.textContent = '✅';
        resultTitle.textContent = 'Connexion Normale';
        resultMessage.textContent = 'Aucune menace détectée. La connexion semble légitime et sécurisée.';
    }
    
    showResult();
}

// ===== GESTION DE L'HISTORIQUE =====
function addToHistory(entry) {
    predictionHistory.unshift(entry);
    
    // Limiter l'historique à 50 entrées
    if (predictionHistory.length > 50) {
        predictionHistory = predictionHistory.slice(0, 50);
    }
    
    saveHistoryToStorage();
    updateHistoryDisplay();
}

function updateHistoryDisplay() {
    if (predictionHistory.length === 0) {
        emptyState.style.display = 'flex';
        historyTable.style.display = 'none';
        return;
    }
    
    emptyState.style.display = 'none';
    historyTable.style.display = 'block';
    
    historyBody.innerHTML = '';
    
    predictionHistory.forEach(entry => {
        const row = document.createElement('tr');
        
        // Formater l'heure
        const time = new Date(entry.timestamp).toLocaleTimeString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        // Créer le badge de statut
        const statusBadge = entry.isAttack 
            ? '<span class="status-badge-table attack">🚨 Attaque</span>'
            : '<span class="status-badge-table normal">✅ Normal</span>';
        
        row.innerHTML = `
            <td>${time}</td>
            <td>${entry.nbPackets}</td>
            <td>${entry.dureeConnexion.toFixed(2)}</td>
            <td>${entry.prediction}</td>
            <td>${statusBadge}</td>
        `;
        
        historyBody.appendChild(row);
    });
}

function clearHistory() {
    if (predictionHistory.length === 0) return;
    
    if (confirm('Êtes-vous sûr de vouloir effacer tout l\'historique ?')) {
        predictionHistory = [];
        saveHistoryToStorage();
        updateHistoryDisplay();
    }
}

// Événement pour le bouton d'effacement
clearHistoryBtn.addEventListener('click', clearHistory);

// ===== STOCKAGE LOCAL =====
function saveHistoryToStorage() {
    try {
        const historyData = predictionHistory.map(entry => ({
            ...entry,
            timestamp: entry.timestamp.toISOString()
        }));
        localStorage.setItem('predictionHistory', JSON.stringify(historyData));
    } catch (error) {
        console.error('Erreur lors de la sauvegarde de l\'historique:', error);
    }
}

function loadHistoryFromStorage() {
    try {
        const stored = localStorage.getItem('predictionHistory');
        if (stored) {
            const parsed = JSON.parse(stored);
            predictionHistory = parsed.map(entry => ({
                ...entry,
                timestamp: new Date(entry.timestamp)
            }));
        }
    } catch (error) {
        console.error('Erreur lors du chargement de l\'historique:', error);
        predictionHistory = [];
    }
}

// ===== FONCTIONS D'AFFICHAGE =====
function showLoader() {
    loader.style.display = 'flex';
    predictBtn.disabled = true;
}

function hideLoader() {
    loader.style.display = 'none';
    predictBtn.disabled = false;
}

function showResult() {
    resultContainer.style.display = 'block';
}

function hideResult() {
    resultContainer.style.display = 'none';
}

function showError(message) {
    errorMessage.innerHTML = message; // Changé pour supporter HTML
    errorContainer.style.display = 'block';
}

function hideError() {
    errorContainer.style.display = 'none';
}

// ===== UTILITAIRES =====
// Log de débogage
console.log('🚀 Application de détection d\'intrusion chargée');
console.log('🔗 API URL:', API_URL);