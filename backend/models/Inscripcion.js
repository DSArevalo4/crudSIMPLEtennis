const mongoose = require('mongoose');

const inscripcionSchema = new mongoose.Schema({
  usuario: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  torneo: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Torneo',
    required: true
  },
  fechaInscripcion: {
    type: Date,
    default: Date.now
  },
  estado: {
    type: String,
    enum: ['activa', 'cancelada'],
    default: 'activa'
  }
}, {
  timestamps: true
});

// Índice compuesto para evitar inscripciones duplicadas
inscripcionSchema.index({ usuario: 1, torneo: 1 }, { unique: true });

module.exports = mongoose.model('Inscripcion', inscripcionSchema);
