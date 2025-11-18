import React, { useState, useEffect } from 'react';
import './GestionInscripciones.css';
import { inscripcionesAPI } from '../../services/api';

const GestionInscripciones = ({ isOpen, onClose }) => {
  const [inscripciones, setInscripciones] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    categoria: '',
    nivel: ''
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    if (isOpen) {
      cargarInscripciones();
    }
  }, [isOpen]);

  const cargarInscripciones = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await inscripcionesAPI.getAll();
      setInscripciones(data);
    } catch (err) {
      setError('Error al cargar inscripciones: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      if (editingId) {
        await inscripcionesAPI.update(editingId, formData);
      } else {
        await inscripcionesAPI.create(formData);
      }
      resetForm();
      cargarInscripciones();
    } catch (err) {
      setError('Error al guardar: ' + err.message);
    }
  };

  const handleEdit = (inscripcion) => {
    setFormData({
      nombre: inscripcion.nombre,
      apellido: inscripcion.apellido,
      email: inscripcion.email,
      telefono: inscripcion.telefono,
      categoria: inscripcion.categoria,
      nivel: inscripcion.nivel
    });
    setEditingId(inscripcion.id);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Estás seguro de eliminar esta inscripción?')) return;
    try {
      await inscripcionesAPI.delete(id);
      cargarInscripciones();
    } catch (err) {
      setError('Error al eliminar: ' + err.message);
    }
  };

  const resetForm = () => {
    setFormData({
      nombre: '',
      apellido: '',
      email: '',
      telefono: '',
      categoria: '',
      nivel: ''
    });
    setEditingId(null);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Gestión de Inscripciones</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="modal-body">
          <form onSubmit={handleSubmit} className="inscripcion-form">
            <h3>{editingId ? 'Editar' : 'Nueva'} Inscripción</h3>
            
            <div className="form-row">
              <input
                type="text"
                name="nombre"
                placeholder="Nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="apellido"
                placeholder="Apellido"
                value={formData.apellido}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <input
                type="tel"
                name="telefono"
                placeholder="Teléfono"
                value={formData.telefono}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <select
                name="categoria"
                value={formData.categoria}
                onChange={handleChange}
                required
              >
                <option value="">Seleccionar Categoría</option>
                <option value="juvenil">Juvenil</option>
                <option value="adulto">Adulto</option>
                <option value="senior">Senior</option>
              </select>

              <select
                name="nivel"
                value={formData.nivel}
                onChange={handleChange}
                required
              >
                <option value="">Seleccionar Nivel</option>
                <option value="principiante">Principiante</option>
                <option value="intermedio">Intermedio</option>
                <option value="avanzado">Avanzado</option>
              </select>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary">
                {editingId ? 'Actualizar' : 'Crear'}
              </button>
              {editingId && (
                <button type="button" className="btn-secondary" onClick={resetForm}>
                  Cancelar
                </button>
              )}
            </div>
          </form>

          <div className="inscripciones-list">
            <h3>Lista de Inscripciones</h3>
            {loading ? (
              <p>Cargando...</p>
            ) : inscripciones.length === 0 ? (
              <p>No hay inscripciones registradas</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Categoría</th>
                    <th>Nivel</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {inscripciones.map((inscripcion) => (
                    <tr key={inscripcion.id}>
                      <td>{inscripcion.nombre} {inscripcion.apellido}</td>
                      <td>{inscripcion.email}</td>
                      <td>{inscripcion.telefono}</td>
                      <td>{inscripcion.categoria}</td>
                      <td>{inscripcion.nivel}</td>
                      <td>
                        <button
                          className="btn-edit"
                          onClick={() => handleEdit(inscripcion)}
                        >
                          ✏️
                        </button>
                        <button
                          className="btn-delete"
                          onClick={() => handleDelete(inscripcion.id)}
                        >
                          🗑️
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GestionInscripciones;
