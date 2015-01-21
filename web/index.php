<?php
require_once('config.php');
$html = '';
$sql = "SELECT * FROM `logs` WHERE 1 ORDER BY `id` desc LIMIT 100 ";
foreach ($pdo->query($sql) as $row) {
	foreach ($row as $key => $value) {
		$row[$key] = htmlspecialchars($value);
	}
	$templete = <<<EOF
        <tr data-toggle="collapse" data-target="#demo{$row['id']}" class="accordion-toggle">
            <td>{$row['id']}</td>
            <td>{$row['method']}</td>
            <td>{$row['rule']}</td>
            <td style="word-break: break-all; word-wrap:break-word;">{$row['url']}</td>
      </th>
        </tr>
        <tr >
            <td colspan="6" class="hiddenRow"><div class="accordian-body collapse" style="word-break: break-all; word-wrap:break-word;" id="demo{$row['id']}">
             <ul>
                <li>{$row['useragent']}</li>
                <li>{$row['raw_data']}</li>
             </ul>

           </div> </td>
EOF;
	$html .= $templete;

}
include_once('templete/index.html');

