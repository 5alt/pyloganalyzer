<?php

$mysql_host = 'localhost';
$mysql_user = 'root';
$mysql_pwd = 'root';
$mysql_db = 'pylog';

$pdo = new PDO ("mysql:host={$mysql_host};dbname={$mysql_db}",$mysql_user,$mysql_pwd);