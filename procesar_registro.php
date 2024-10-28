<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Recibir el email desde el formulario
    $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);

    // Validar el email
    if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
        // Tu API Key de Mailchimp
        $apiKey = '1ca1eebd09d13821bc9851f2759385d3-us8';
        // ID de la lista a la que añadirás los suscriptores
        $listId = '9976ea0bb8';
        // Extraer el datacenter desde la API Key
        $dataCenter = substr($apiKey, strpos($apiKey, '-')+1);
        
        // URL de la API para agregar suscriptores
        $url = 'https://' . $dataCenter . '.api.mailchimp.com/3.0/lists/' . $listId . '/members/';
        
        // Preparar los datos en formato JSON
        $jsonData = json_encode([
            'email_address' => $email,
            'status'        => 'subscribed'
        ]);

        // Iniciar cURL para hacer la petición a Mailchimp
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_USERPWD, 'user:' . $apiKey);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);

        // Ejecutar la petición y cerrar cURL
        $result = curl_exec($ch);
        curl_close($ch);

        // Verificar si la suscripción fue exitosa
        if ($result) {
            echo "Gracias por suscribirte.";
        } else {
            echo "Hubo un problema, por favor intenta más tarde.";
        }
    } else {
        echo "Email inválido. Por favor ingresa un email válido.";
    }
}
