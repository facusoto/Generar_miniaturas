document.addEventListener("DOMContentLoaded", () => {
  const backgroundSection = document.querySelector(".background-options"); // Contenedor de "Fondo"
  const personsSection = document.querySelector(".person-options"); // Contenedor de "Personas recortadas"

  const imageInput = document.getElementById("imageInput");

  // Función para manejar la carga de una imagen en un espacio específico
  const handleImageLoad = (file, optionItem) => {
    const reader = new FileReader();
    reader.onload = () => {
      optionItem.innerHTML = `<img src="${reader.result}" alt="Imagen cargada">`;
    };
    reader.readAsDataURL(file);
  };

  // Función para manejar múltiples imágenes
  const handleMultipleImages = (files, targetSection) => {
    const optionItems = targetSection.querySelectorAll(".option-item");
    const availableSlots = [...optionItems].filter(item => !item.querySelector("img")); // Espacios vacíos
    const filesToUse = Array.from(files).slice(0, availableSlots.length); // Máximo número de archivos permitido

    filesToUse.forEach((file, index) => {
      handleImageLoad(file, availableSlots[index]);
    });

    if (files.length > availableSlots.length) {
      alert(`Se ignoraron ${files.length - availableSlots.length} imágenes excedentes.`);
    }
  };

  // Manejar el input de archivo
  imageInput.addEventListener("change", (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      // Verifica si el input fue activado desde "Personas recortadas"
      const isPersonsSection = imageInput.dataset.section === "persons";
      const targetSection = isPersonsSection ? personsSection : backgroundSection;
      handleMultipleImages(files, targetSection);
    }
    imageInput.value = ""; // Resetea el input para permitir nuevas cargas
  });

  // Asignar eventos de clic y arrastrar/soltar a cada sección
  const setupSection = (section, sectionName) => {
    const optionItems = section.querySelectorAll(".option-item");

    // Evento de clic para abrir el selector de archivos
    optionItems.forEach((item) => {
      item.addEventListener("click", () => {
        imageInput.dataset.section = sectionName; // Define la sección activa
        imageInput.click();
      });
    });

    // Eventos de arrastrar y soltar
    section.addEventListener("dragover", (event) => {
      event.preventDefault();
      section.style.borderColor = "#4caf50"; // Cambia el borde al arrastrar
    });

    section.addEventListener("dragleave", () => {
      section.style.borderColor = "transparent"; // Restaura el borde
    });

    section.addEventListener("drop", (event) => {
      event.preventDefault();
      section.style.borderColor = "transparent"; // Restaura el borde

      const files = event.dataTransfer.files;
      if (files.length > 0) {
        handleMultipleImages(files, section);
      }
    });
  };

  // Configurar las dos secciones
  setupSection(backgroundSection, "background");
  setupSection(personsSection, "persons");
});

document.addEventListener("DOMContentLoaded", () => {
  const personsSection = document.querySelector(".person-options");
  const backgroundSection = document.querySelector(".background-options");
  const processButton = document.getElementById("processButton");
  const imageInput = document.getElementById("imageInput");

  // Mostrar indicador de carga
  const showLoadingIndicator = (optionItem) => {
    const loader = document.createElement("div");
    loader.className = "loading-overlay";
    loader.innerHTML = `<div class="loading-indicator">⌛</div>`;
    optionItem.appendChild(loader);
  };

  // Procesar imágenes de una sección específica
  const processSectionImages = async (section, endpoint) => {
    const optionItems = section.querySelectorAll(".option-item img");

    for (const item of optionItems) {
      const parent = item.closest(".option-item");

      // Mostrar indicador de carga sin eliminar la imagen original
      showLoadingIndicator(parent);

      const imageBlob = await fetch(item.src).then((res) => res.blob());
      const formData = new FormData();
      formData.append("image", imageBlob, "image.png");

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const processedBlob = await response.blob();
          const processedURL = URL.createObjectURL(processedBlob);

          // Reemplaza la imagen actual y elimina el indicador
          item.src = processedURL;
        } else {
          console.error(`Error procesando la imagen en ${endpoint}.`);
        }
      } catch (error) {
        console.error(`Error al enviar la imagen a ${endpoint}:`, error);
      } finally {
        // Eliminar el indicador de carga
        const loader = parent.querySelector(".loading-overlay");
        if (loader) loader.remove();
      }
    }
  };

  // Manejar el clic en el botón de procesamiento
  processButton.addEventListener("click", () => {
    processSectionImages(personsSection, "/process-people");
    processSectionImages(backgroundSection, "/process-background");
  });

  // Manejar el input de archivo
  imageInput.addEventListener("change", (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      const optionItems = personsSection.querySelectorAll(".option-item");
      const availableSlots = [...optionItems].filter((item) => !item.querySelector("img"));
      const filesToUse = Array.from(files).slice(0, availableSlots.length);

      filesToUse.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = () => {
          availableSlots[index].innerHTML = `<img src="${reader.result}" alt="Imagen cargada">`;
        };
        reader.readAsDataURL(file);
      });

      if (files.length > availableSlots.length) {
        alert(`Se ignoraron ${files.length - availableSlots.length} imágenes excedentes.`);
      }
    }
    imageInput.value = ""; // Resetea el input
  });
});
