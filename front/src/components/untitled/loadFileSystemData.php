<?php
if(!isset($_POST['isFirst']))
{
	echo json_encode(['success' => 0, 'error' => 'Отсутствуют необходимые аргументы']);
	return;
}

if($_POST['isFirst'] == 'true')
	loadFirst();
else
{
	if(!isset($_POST['parentPath']))
	{
		echo json_encode(['success' => 0, 'error' => 'Отсутствуют необходимые аргументы']);
		return;
	}
	loadSubFolders();
}

function loadFirst() : void
{
	$fso = new COM('Scripting.FileSystemObject');
	$drives = $fso->Drives;
	/*
	 * 'Unknown', 'Removable', 'Fixed', 'Network', 'CD-ROM', 'RAM Disk'
	 * */
	$arr = '<ul>';
	foreach($drives as $drive)
	{
		$d = $fso->GetDrive($drive);
		if($d->DriveType == 2)
			$arr .= '<li class="root-drive" data-path="'.$d->RootFolder->Path.'"><span>'.$d->RootFolder->Path.'</span></li>';
	}
	$arr .= '</ul>';
	
	echo json_encode(['success' => 1, 'drives' => $arr]);
}
function loadSubFolders() : void{
	$parent = $_POST['parentPath'];
	$parent = html_entity_decode($parent);
	
	$arr = '';
	$fso = new COM('Scripting.FileSystemObject', null, 1251);
	define('READ_ONLY', 1);
	define('IS_HIDDEN', 2);
	define('IS_SYSTEM', 4);
	
	$dirs = glob($parent.'/*', GLOB_ONLYDIR);
	foreach($dirs as $dir)
	{
		try
		{
			$folder = $fso->getfolder($dir);
			if(($folder->Attributes & IS_HIDDEN) <> 0)
				continue;
			if(($folder->Attributes & IS_SYSTEM) <> 0)
				continue;
		}
		catch(Exception $e)
		{
			continue;
		}
		
		$arr .= '<li data-path="'.htmlentities($dir).'"><span>'.basename($dir).'</span></li>';
	}
	
	if(strlen($arr) > 0)
	{
		$arr = '<ul class="sublist">'.$arr;
		$arr .= '</ul>';
	}
	
	echo json_encode(['success' => 1, 'folders' => $arr]);
}