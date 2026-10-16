$ErrorActionPreference = "Stop"
try {
    $pptApp = New-Object -ComObject PowerPoint.Application
    
    $files = @(
        @{ Pptx = "C:\Users\lenovo\Desktop\graph_visualization\Correlation_Network_Studio_Presentation.pptx"; Pdf = "C:\Users\lenovo\Desktop\graph_visualization\Correlation_Network_Studio_Presentation.pdf" },
        @{ Pptx = "C:\Users\lenovo\Desktop\graph_visualization\presentation.pptx"; Pdf = "C:\Users\lenovo\Desktop\graph_visualization\presentation.pdf" },
        @{ Pptx = "C:\Users\lenovo\Desktop\graph_visualization\correlation_network_presentation.pptx"; Pdf = "C:\Users\lenovo\Desktop\graph_visualization\correlation_network_presentation.pdf" }
    )

    foreach ($item in $files) {
        $pptxPath = $item.Pptx
        $pdfPath = $item.Pdf
        Write-Host "Opening presentation: $pptxPath"
        $presentation = $pptApp.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
        Write-Host "Exporting to PDF: $pdfPath"
        # 32 represents ppSaveAsPDF
        $presentation.SaveAs($pdfPath, 32)
        $presentation.Close()
        Write-Host "SUCCESS: Generated $pdfPath"
    }

    $pptApp.Quit()
    Write-Host "ALL PDFs EXPORTED SUCCESSFULLY!"
} catch {
    Write-Error $_.Exception.Message
    if ($pptApp) { $pptApp.Quit() }
    exit 1
}
