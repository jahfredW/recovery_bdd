<?php

$host = "localhost";
$user = "root";
$password = "";
$backupPath = 'C:/test';

// Récupérer la liste des bases de données
$command = "mysql -h $host -u $user -e \"SHOW DATABASES;\"";
$databases = shell_exec($command);


$databases = explode("\n", trim($databases));



// Exclure certaines bases de données
$excludeDatabases = ['information_schema', 'performance_schema', 'mysql', 'Database'];
$databases = array_diff($databases, $excludeDatabases);



if(!file_exists($backupPath))
{
    mkdir($backupPath, 0777, true);
}

// Dump de chaque base de données
foreach ($databases as $database) {
    $dumpFile = $backupPath . '/backup_' . $database . '.sql';
    $command = "mysqldump -h $host -u $user $database > $dumpFile";
    
    exec($command, $output, $return_var);
    
    if ($return_var === 0) {
        echo "Sauvegarde de $database réussie.\n";
    } else {
        echo "Erreur pendant la sauvegarde de $database.\n";
    }
}
