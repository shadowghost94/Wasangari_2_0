document.getElementById('dash-modif-profil1').addEventListener('click', function() {
    // Masquer toutes les sections grid-item
    document.querySelectorAll('.div-dashboard-principale').forEach(function(item) {
        item.style.display = 'none';
    });
    document.getElementById('affiche-things').style.display = 'none';
    document.getElementById('modif-afficher').style.display = 'block';
});

document.getElementById('back-to-main1').addEventListener('click', function() {
    // Afficher toutes les sections grid-item
    document.querySelectorAll('.div-dashboard-principale').forEach(function(item) {
        item.style.display = 'flex';
    });
    document.getElementById('affiche-things').style.display = 'block';
    document.getElementById('modif-afficher').style.display = 'none';
});

//permet de visualiser une photo sélectionné
function previewProfilePic(event) {
    const reader = new FileReader();
    reader.onload = function() {
        const output = document.getElementById('profile-pic-das');
        output.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}

//enregistrement des nouvelles informations
document.getElementById('profile-form-das').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    console.log(formData);
    $.ajax({
        url: '{% url "modifierProfil" %}',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        success: function(response) {
            if (response.success) {
                document.getElementById('responseMessage').innerText = 'Votre profil a été modifié avec succès';
            } else {
                document.getElementById('responseMessage').innerText = 'Une erreur medium est survenue lors de la mise à jour du profil';
            }
        },
        error: function() {
            document.getElementById('responseMessage').innerText = 'Une erreur est survenue lors de la mise à jour du profil';
        }
    });
});


/* Concerne l'affichage du formulaire d'ajout d'event */
document.getElementById('addEvent').addEventListener('click', function() {
    // Masquer toutes les sections grid-item
    document.querySelectorAll('.div-dashboard-principale').forEach(function(item) {
        item.style.display = 'none';
    });
    document.getElementById('affiche-things').style.display = 'none';
    document.getElementById('ajoutEvent').style.display = 'block';
});

document.getElementById('retour1').addEventListener('click', function() {
     // Afficher toutes les sections grid-item
     document.querySelectorAll('.div-dashboard-principale').forEach(function(item) {
         item.style.display = 'flex';
     });
     document.getElementById('affiche-things').style.display = 'block';
     document.getElementById('ajoutEvent').style.display = 'none';
 });


 /* Concerne l'affichage du formulaire d'ajout d'objet à vendre */
document.getElementById('addObjet').addEventListener('click', function() {
    // Masquer toutes les sections grid-item
    document.querySelectorAll('.div-dashboard-principale').forEach(function(item) {
        item.style.display = 'none';
    });
    document.getElementById('affiche-things').style.display = 'none';
    document.getElementById('ajoutObjet').style.display = 'block';
});

document.getElementById('retour2').addEventListener('click', function() {
     // Afficher toutes les sections grid-item
     document.querySelectorAll('.div-dashboard-principale').forEach(function(item) {
         item.style.display = 'flex';
     });
     document.getElementById('affiche-things').style.display = 'block';
     document.getElementById('ajoutObjet').style.display = 'none';
 });

 /* Concerne l'affichage du formulaire d'ajout de nouvel actualité */
 document.getElementById('addNews').addEventListener('click', function() {
    // Masquer toutes les sections grid-item
    document.querySelectorAll('.div-dashboard-principale').forEach(function(item) {
        item.style.display = 'none';
    });
    document.getElementById('affiche-things').style.display = 'none';
    document.getElementById('ajoutNews').style.display = 'block';
});

document.getElementById('retour3').addEventListener('click', function() {
     // Afficher toutes les sections grid-item
     document.querySelectorAll('.div-dashboard-principale').forEach(function(item) {
         item.style.display = 'flex';
     });
     document.getElementById('affiche-things').style.display = 'block';
     document.getElementById('ajoutNews').style.display = 'none';
 });


 // ajax-form.js
$(document).ready(function() {
    $('#profile-form-event').submit(function(event) {
        event.preventDefault();

        var formData = new FormData($(this)[0]);

        $.ajax({
            url: '/addEvent/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log('Données soumises avec succès');
            },
            error: function(xhr, status, error) {
                console.error('Erreur:', error);
            }
        });
    });

    
});

// ajouter un objet en vente
$(document).ready(function(){
    $('#profile-form-objet').submit(function(event) {
        event.preventDefault();

        var formData = new FormData($(this)[0]);

        $.ajax({
            url: '/addObjet/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log('Données soumises avec succès');
            },
            error: function(xhr, status, error) {
                console.error('Erreur:', error);
            }
        });
    });
});

// ajouter une actualité
$(document).ready(function(){
    $('#profile-form-news').submit(function(event) {
        event.preventDefault();

        var formData = new FormData($(this)[0]);

        $.ajax({
            url: '/addNews/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log('Données soumises avec succès');
            },
            error: function(xhr, status, error) {
                console.error('Erreur:', error);
            }
        });
    });
});