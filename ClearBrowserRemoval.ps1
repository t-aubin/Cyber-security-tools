# This script is used to REMOVE the presence of Clear, ClearBrowser, ClearBar, OneLaunch, and Chromium on devices

# CLEAR REMOVAL SCRIPT (USE CAUTION!!!!):

# find running processes with "clear" in them

$valid_clear_path = "C:\Users\*\AppData\Local\*"

$clear_processes = Get-Process | Where-Object { $_.Name -like "*clear*" }

if ($clear_processes.Count -eq 0){

Write-Output "No Clear processes were found."

}

else {

write-output "The following processes contained Clear and file paths will be checked: $clear_processes"

foreach ($process in $clear_processes){

$path = $process.Path

if ($path -like $valid_clear_path){

Stop-Process $process -Force

Write-Output "$process.Name process file path matches and has been stopped."

}

else {

Write-Output "$process.Name file path doesn't match and process was not stopped."

}

}

Start-Sleep -Seconds 2

}

$file_paths = @("\appdata\local\clear", "\appdata\local\clearbar", "\appdata\local\clearbrowser", "\appdata\local\programs\clear", "\appdata\local\programs\clearbar", "\appdata\local\temp\clearbrowser_topsites", "\appdata\roaming\microsoft\windows\start menu\programs\clear.lnk", "\appdata\roaming\microsoft\windows\start menu\programs\clearbar.lnk", "\desktop\clear.lnk", "\desktop\clearbar.lnk")

# iterate through users for clear related directories

foreach ($folder in (get-childitem c:\users)) {

foreach ($fpath in $file_paths){

$path = $folder.pspath + $fpath

if (test-path $path) {

Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue

write-output "$path has been deleted."

}

}

}

$reg_paths = @("\software\clearbar", "\software\clearbar.app", "\software\clearbrowser")

# iterate through users for clear related registry keys

foreach ($registry_hive in (get-childitem registry::hkey_users)) {

foreach ($regpath in $reg_paths){

$path = $registry_hive.pspath + $regpath

if (test-path $path) {

Remove-item -Path $path -Recurse -Force

write-output "$path has been removed."

}

}

}

$reg_properties = @("clearbar", "clearbar.app", "clearbrowser", "clear")

foreach($registry_hive in (get-childitem registry::hkey_users)){

foreach ($property in $reg_properties){

$path = $registry_hive.pspath + "\software\microsoft\windows\currentversion\run"

if (test-path $path){

$reg_key = Get-Item $path

if ($reg_key.GetValue($property)){

Remove-ItemProperty $path $property

Write-output "$path\$property registry property value has been removed."

}

}

}

}

$schtasknames = @("ClearStartAtLoginTask", "ClearbarStartAtLoginTask", "ClearUpdateChecker", "ClearbarUpdateChecker")

$c = 0

# find clear related scheduled tasks

foreach ($task in $schtasknames){

$clear_tasks = get-scheduledtask -taskname $task -ErrorAction SilentlyContinue

if ($clear_tasks){

$c++

Unregister-ScheduledTask -TaskName $task -Confirm:$false

Write-Output "Scheduled task '$task' has been removed."

}

}

if ($c -eq 0){

Write-Output "No Clear scheduled tasks were found."

}
