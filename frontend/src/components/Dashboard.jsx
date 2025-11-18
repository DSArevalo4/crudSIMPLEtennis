import React, { useState } from 'react';
import GestionInscripciones from './Inscripciones/GestionInscripciones';
import './Dashboard.css';

const Dashboard = () => {
  const [showInscripciones, setShowInscripciones] = useState(false);

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <h2>Menú</h2>
        <nav>
          <button 
            className="menu-item"
            onClick={() => setShowInscripciones(true)}
          >
            <span className="icon">📋</span>
            <span>Inscripciones</span>
          </button>
          {/* Agregar más items de menú aquí */}
        </nav>
      </aside>

      <div className="main-content">
        <header className="dashboard-header">
          <h1>Dashboard - Club de Tenis</h1>
        </header>
        
        <main className="dashboard-main">
          <section className="dashboard-card">
            <h2>Inicio</h2>
            <p>Bienvenido al sistema de gestión del club de tenis.</p>
          </section>
          
          <section className="dashboard-card">
            <h2>Inscripciones</h2>
            <p>Administra las inscripciones de los jugadores.</p>
            <button 
              className="btn-action"
              onClick={() => setShowInscripciones(true)}
            >
              Abrir Gestión de Inscripciones
            </button>
          </section>
        </main>
        
        <footer className="dashboard-footer">
          <p>© 2024 Club de Tenis - Sistema de Gestión</p>
        </footer>
      </div>

      <GestionInscripciones 
        isOpen={showInscripciones} 
        onClose={() => setShowInscripciones(false)} 
      />
    </div>
  );
};

export default Dashboard;