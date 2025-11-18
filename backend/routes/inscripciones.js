const express = require('express');
const router = express.Router();
const Inscripcion = require('../models/Inscripcion');
const Torneo = require('../models/Torneo');
const User = require('../models/User');
const auth = require('../middleware/auth');

// Obtener todas las inscripciones
router.get('/', auth, async (req, res) => {
  try {
    const inscripciones = await Inscripcion.find()
      .populate('usuario', 'username email perfil')
      .populate('torneo', 'nombre fechaInicio fechaFin estado');
    res.json(inscripciones);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Obtener inscripciones por torneo
router.get('/torneo/:torneoId', auth, async (req, res) => {
  try {
    const inscripciones = await Inscripcion.find({ 
      torneo: req.params.torneoId,
      estado: 'activa'
    }).populate('usuario', 'username email perfil');
    res.json(inscripciones);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Obtener inscripciones por usuario
router.get('/usuario/:usuarioId', auth, async (req, res) => {
  try {
    const inscripciones = await Inscripcion.find({ 
      usuario: req.params.usuarioId,
      estado: 'activa'
    }).populate('torneo', 'nombre fechaInicio fechaFin estado');
    res.json(inscripciones);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Crear inscripción
router.post('/', auth, async (req, res) => {
  try {
    const { usuarioId, torneoId } = req.body;
    
    // Verificar que el torneo existe
    const torneo = await Torneo.findById(torneoId);
    if (!torneo) {
      return res.status(404).json({ message: 'Torneo no encontrado' });
    }
    
    // Verificar que el usuario existe
    const usuario = await User.findById(usuarioId);
    if (!usuario) {
      return res.status(404).json({ message: 'Usuario no encontrado' });
    }
    
    // Validar permisos según el perfil
    if (req.user.perfil === 'deportista') {
      // Los deportistas solo pueden inscribirse a sí mismos
      if (req.user.id !== usuarioId) {
        return res.status(403).json({ 
          message: 'Los deportistas solo pueden inscribirse a sí mismos' 
        });
      }
      
      // Los deportistas solo pueden inscribirse a torneos abiertos
      if (torneo.estado !== 'abierto') {
        return res.status(403).json({ 
          message: 'Solo puedes inscribirte a torneos abiertos' 
        });
      }
    }
    
    // Verificar si ya existe una inscripción activa
    const inscripcionExistente = await Inscripcion.findOne({
      usuario: usuarioId,
      torneo: torneoId,
      estado: 'activa'
    });
    
    if (inscripcionExistente) {
      return res.status(400).json({ 
        message: 'Ya existe una inscripción activa para este torneo' 
      });
    }
    
    const inscripcion = new Inscripcion({
      usuario: usuarioId,
      torneo: torneoId
    });
    
    const nuevaInscripcion = await inscripcion.save();
    const inscripcionPopulada = await Inscripcion.findById(nuevaInscripcion._id)
      .populate('usuario', 'username email perfil')
      .populate('torneo', 'nombre fechaInicio fechaFin estado');
    
    res.status(201).json(inscripcionPopulada);
  } catch (error) {
    if (error.code === 11000) {
      res.status(400).json({ message: 'Ya existe una inscripción para este usuario en este torneo' });
    } else {
      res.status(400).json({ message: error.message });
    }
  }
});

// Eliminar inscripción (cancelar)
router.delete('/:id', auth, async (req, res) => {
  try {
    const inscripcion = await Inscripcion.findById(req.params.id);
    
    if (!inscripcion) {
      return res.status(404).json({ message: 'Inscripción no encontrada' });
    }
    
    // Los deportistas solo pueden cancelar sus propias inscripciones
    if (req.user.perfil === 'deportista' && inscripcion.usuario.toString() !== req.user.id) {
      return res.status(403).json({ 
        message: 'No tienes permiso para cancelar esta inscripción' 
      });
    }
    
    await Inscripcion.findByIdAndDelete(req.params.id);
    res.json({ message: 'Inscripción cancelada exitosamente' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
