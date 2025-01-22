document
    .getElementById("formulaire-inscription")
    .addEventListener("submit", async function (event) {
        event.preventDefault(); // Empêche le rechargement de la page et la soumission par défaut

        const formData = new FormData(event.target); // Récupère les données du formulaire

        // Convertir les données du formulaire en objet JSON
        const data = Object.fromEntries(formData.entries());

        // Envoyer les données via fetch
        try {
            const response = await fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            // Gérer la réponse
            const messageElement = document.getElementById("responseMessage");
            if (response.ok) {
                messageElement.style.color = "green";
                messageElement.textContent =
                    "Inscription réussie ! Bienvenue, " + result.username + ".";
            } else {
                messageElement.style.color = "red";
                messageElement.textContent = "Erreur : " + result.message;
            }
        } catch (error) {
            // En cas d'erreur réseau
            const messageElement = document.getElementById("responseMessage");
            messageElement.style.color = "red";
            messageElement.textContent =
                "Erreur de connexion. Veuillez réessayer.";
        }
    });
