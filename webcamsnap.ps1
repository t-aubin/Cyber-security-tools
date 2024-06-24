# Add necessary AForge.NET libraries
Add-Type -Path "C:\AForge\AForge.Video.dll"
Add-Type -Path "C:\AForge\AForge.Video.DirectShow.dll"

# Create a video capture device class
$videoCaptureDevice = New-Object AForge.Video.DirectShow.VideoCaptureDevice

# Find available video devices
$videoDevices = New-Object AForge.Video.DirectShow.FilterInfoCollection([AForge.Video.DirectShow.FilterCategory]::VideoInputDevice)

if ($videoDevices.Count -eq 0) {
    Write-Host "No video devices found."
    exit
}

# Select the first available device
$videoCaptureDevice = New-Object AForge.Video.DirectShow.VideoCaptureDevice($videoDevices[0].MonikerString)

# Define the event to be triggered when a new frame is available
$FrameEventHandler = {
    param($sender, $eventArgs)
    
    # Retrieve the current frame
    $bitmap = $eventArgs.Frame.Clone()

    # Save the frame as a JPEG file
    $outputPath = "C:\temp\webcam_image.jpg"
    $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)

    # Signal to stop the video capture
    $videoCaptureDevice.SignalToStop()
    
    Write-Host "Image captured and saved to $outputPath"
}

# Attach the event handler
$videoCaptureDevice.NewFrame.Add($FrameEventHandler)

# Start capturing video
$videoCaptureDevice.Start()

# Wait for a few seconds to capture the image
Start-Sleep -Seconds 5

# Stop capturing video (in case the event didn't trigger properly)
if ($videoCaptureDevice.IsRunning) {
    $videoCaptureDevice.SignalToStop()
}

# Cleanup
$videoCaptureDevice.WaitForStop()
