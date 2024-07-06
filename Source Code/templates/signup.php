<?php
$servername = "localhost";
$username = "your_username";
$password = "your_password";
$dbname = "data1.db";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $newUsername = $_POST["newUsername"];
    $newPassword = $_POST["newPassword"];
    $name = $_POST["name"];
    $age = $_POST["age"];

    // Handle file upload
    $voiceRecording = $_FILES["voiceRecording"]["tmp_name"];
    $voiceRecordingData = file_get_contents($voiceRecording);

    $stmt = $conn->prepare("INSERT INTO users (username, password, name, age, voiceRecording) VALUES (?, ?, ?, ?, ?)");
    $stmt->bind_param("sssis", $newUsername, $newPassword, $name, $age, $voiceRecordingData);

    if ($stmt->execute()) {
        echo "User registered successfully!";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
}

$conn->close();
?>
