'''
Extend the unallocated drives on the VM

'''



# Create a temporary script file for Diskpart commands
$ScriptFilePath = Join-Path -Path $env:TEMP -ChildPath 'diskpart_script.txt'
# path C:\Users\Support\AppData\Local\Temp\diskpart_script.txt
# Get the current size of the C drive
$CDrive = Get-Partition | Where-Object { $_.DriveLetter -eq 'C' }
$CurrentSizeMB = $CDrive.Size / 1MB
Write-Host "Current size of C drive: $CurrentSizeMB MB"
# Define the Diskpart commands to extend the partition
$DiskpartCommands = @"
select disk 0
select partition 1
extend
"@
# Write the Diskpart commands to the script file
$DiskpartCommands | Set-Content -Path $ScriptFilePath
# Execute Diskpart with the script file
Start-Process -FilePath 'diskpart' -ArgumentList "/s $ScriptFilePath" -Wait
# Remove the temporary script file
Remove-Item -Path $ScriptFilePath -Force


# repeat the process with d drive
$ScriptFilePath = Join-Path -Path $env:TEMP -ChildPath 'diskpart_script.txt'
# path C:\Users\Support\AppData\Local\Temp\diskpart_script.txt
# Get the current size of the D drive
$DDrive = Get-Partition | Where-Object { $_.DriveLetter -eq 'D' }
$CurrentSizeDMB = $DDrive.Size / 1MB
Write-Host "Current size of D drive: $CurrentSizeDMB MB"
# Define the Diskpart commands to extend the partition
$DiskpartCommands = @"
select disk 1
select partition 1
extend
"@
# Write the Diskpart commands to the script file
$DiskpartCommands | Set-Content -Path $ScriptFilePath
# Execute Diskpart with the script file
Start-Process -FilePath 'diskpart' -ArgumentList "/s $ScriptFilePath" -Wait
# Remove the temporary script file
Remove-Item -Path $ScriptFilePath -Force


# Get the new size of the C drive
$CDrive = Get-Partition | Where-Object { $_.DriveLetter -eq 'C' }
$NewSizeMB = $CDrive.Size / 1MB
#if the size is the same, then the partition was not extended, else it was
if ($NewSizeMB -eq $CurrentSizeMB) {
    Write-Host "The C drive was not extended."
    Write-Host "the size of C drive is still : $NewSizeMB MB"
} else {
    Write-Host "The C drive size was altered."
    Write-Host "New size of C drive: $NewSizeMB MB"
}

# Get the new size of the D drive
$DDrive = Get-Partition | Where-Object { $_.DriveLetter -eq 'D' }
$NewSizeDMB = $DDrive.Size / 1MB
#if the size is the same, then the partition was not extended, else it was
if ($NewSizeDMB -eq $CurrentSizeDMB) {
    Write-Host "The D drive was not extended."
    Write-Host "the size of D drive is still : $NewSizeDMB MB"
} else {
    Write-Host "The D drive size was altered."
    Write-Host "New size of D drive: $NewSizeDMB MB"
}



