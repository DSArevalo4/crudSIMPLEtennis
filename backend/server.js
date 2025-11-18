const express = require('express');
const app = express();
const inscripcionesRouter = require('./routes/inscripciones');

app.use('/api/inscripciones', inscripcionesRouter);