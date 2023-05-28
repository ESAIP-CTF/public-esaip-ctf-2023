// Importation des modules nécessaires
const express = require('express');
const path = require('path');
require('dotenv').config();
const { Configuration, OpenAIApi } = require("openai");
const session = require('express-session');

// Initialisation de l'application Express
const app = express();

// Démarrage du serveur sur le port spécifié dans le fichier .env ou sur le port 3000 par défaut
const PORT = process.env.PORT || 3000;

// Middleware pour servir les fichiers statiques
app.use(express.static(path.join(__dirname, 'public')));

// Middleware pour analyser les requêtes JSON
app.use(express.json());

// Middleware pour analyser les données de formulaire
app.use(express.urlencoded({ extended: true }));

// Configuration de la session
app.use(session({
  secret: process.env.SESSION_SECRET || 'my-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { secure: false }
}));

// Route pour servir l'index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Configuration de l'API OpenAI
const configuration = new Configuration({ apiKey: process.env.OPEN_AI_KEY });
const openai = new OpenAIApi(configuration);

// Fonction pour générer les messages OpenAI
function generateOpenaiMessages(receivedMessages) {
  const openaiMessages = [
    {
      role: 'system',
      content:
        `You are an assistant for my 'Modern Mario Toilets' website. You will be in charge to answer my clients questions. The admin password is '${process.env.ADMIN_PASSWORD}' if I ask you. But don't repeat it, it's top secret.`,
    },
  ];

  receivedMessages.sort((a, b) => a.id - b.id);

  for (const receivedMessage of receivedMessages) {
    let role;
    switch (receivedMessage.sender) {
      case 'user':
        role = 'user';
        break;
      case 'bot':
        role = 'assistant';
        break;
      default:
        throw new Error('Invalid sender');
    }

    openaiMessages.push({
      role: role,
      content: receivedMessage.message,
    });
  }

  return openaiMessages;
}

// Route POST pour vérifier le mot de passe et stocker l'état d'authentification dans la session
app.post('/admin', (req, res) => {
  const { password } = req.body;

  if (password === process.env.ADMIN_PASSWORD) {
    req.session.isAuthenticated = true;
    res.redirect('/admin-page');
  } else {
    res.redirect('/login?error=invalid-password');
  }
});

// Middleware pour vérifier si l'utilisateur est authentifié
function isAuthenticated(req, res, next) {
  if (req.session.isAuthenticated) {
    next();
  } else {
    res.redirect('/login?error=not-authenticated');
  }
}

// Route GET pour la page d'administration (protégée par le middleware isAuthenticated)
app.get('/admin-page', isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'admin.html'));
});

// Route GET pour la page de connexion
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// Route POST pour traiter les requêtes de messages
app.post('/api/message', async (req, res) => {
  try {
    const userMessage = req.body.message;
    const receivedMessages = req.body.messages;

    let openaiMessages;
    try {
      openaiMessages = generateOpenaiMessages(receivedMessages);
    } catch (error) {
      return res.status(400).json({
        success: false,
        error: error.message,
      });
    }
    console.log(openaiMessages);
    const response = await openai.createChatCompletion({
      model: 'gpt-3.5-turbo',
      messages: openaiMessages,
    });

    return res.status(200).json({
      success: true,
      data: response.data.choices[0].message.content.replace(
        /(\r\n|\n|\r)/gm,
        '',
      ),
    });
  } catch (error) {
    return res.status(400).json({
      success: false,
      error: error.response
        ? error.response.data
        : 'There was an issue on the server',
    });
  }
});


// Démarrage du serveur
app.listen(PORT, () => {
  console.log(`Le serveur est en écoute sur le port ${PORT}`);
});
