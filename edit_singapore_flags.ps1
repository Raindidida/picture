Add-Type -AssemblyName System.Drawing

function New-StarPoints {
    param(
        [double]$cx,
        [double]$cy,
        [double]$outer,
        [double]$inner
    )

    $points = New-Object System.Collections.Generic.List[System.Drawing.PointF]
    for ($i = 0; $i -lt 10; $i++) {
        $angle = -[Math]::PI / 2 + $i * [Math]::PI / 5
        $radius = if ($i % 2 -eq 0) { $outer } else { $inner }
        $points.Add([System.Drawing.PointF]::new(
            [single]($cx + [Math]::Cos($angle) * $radius),
            [single]($cy + [Math]::Sin($angle) * $radius)
        ))
    }
    return $points.ToArray()
}

function Draw-SingaporeFlag {
    param(
        [System.Drawing.Graphics]$Graphics,
        [float]$X,
        [float]$Y,
        [float]$W,
        [float]$H
    )

    $red = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(238, 45, 56))
    $white = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
    $border = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(160, 220, 230, 240), [Math]::Max(1, $H * 0.035))

    $Graphics.FillRectangle($red, $X, $Y, $W, $H / 2)
    $Graphics.FillRectangle($white, $X, $Y + $H / 2, $W, $H / 2)

    $cx = $X + $W * 0.245
    $cy = $Y + $H * 0.255
    $outer = $H * 0.19
    $Graphics.FillEllipse($white, $cx - $outer, $cy - $outer, $outer * 2, $outer * 2)
    $Graphics.FillEllipse($red, $cx - $outer * 0.45, $cy - $outer, $outer * 2, $outer * 2)

    $starOuter = [Math]::Max(1.25, $H * 0.045)
    $starInner = $starOuter * 0.42
    $starCx = $X + $W * 0.38
    $starCy = $Y + $H * 0.255
    $r = $H * 0.125
    $starPositions = @(
        @($starCx, $starCy - $r),
        @($starCx + $r * 0.95, $starCy - $r * 0.32),
        @($starCx + $r * 0.6, $starCy + $r * 0.8),
        @($starCx - $r * 0.6, $starCy + $r * 0.8),
        @($starCx - $r * 0.95, $starCy - $r * 0.32)
    )
    foreach ($pos in $starPositions) {
        $Graphics.FillPolygon($white, (New-StarPoints $pos[0] $pos[1] $starOuter $starInner))
    }

    $Graphics.DrawRectangle($border, $X, $Y, $W, $H)

    $red.Dispose()
    $white.Dispose()
    $border.Dispose()
}

function Edit-Image {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [array]$Flags,
        [scriptblock]$ExtraDraw
    )

    $bitmap = [System.Drawing.Bitmap]::FromFile($InputPath)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

    foreach ($flag in $Flags) {
        Draw-SingaporeFlag $graphics $flag[0] $flag[1] $flag[2] $flag[3]
    }

    if ($null -ne $ExtraDraw) {
        & $ExtraDraw $graphics
    }

    $extension = [System.IO.Path]::GetExtension($OutputPath).ToLowerInvariant()
    $format = if ($extension -eq ".png") { [System.Drawing.Imaging.ImageFormat]::Png } else { [System.Drawing.Imaging.ImageFormat]::Jpeg }
    $bitmap.Save($OutputPath, $format)
    $graphics.Dispose()
    $bitmap.Dispose()
}

$outDir = "E:\picture2\edited_flags"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

Edit-Image `
    -InputPath "C:\Users\1212\AppData\Local\Temp\codex-clipboard-74edc883-f554-4ae4-9381-d557ea24921d.png" `
    -OutputPath "$outDir\image1-byteforge-singapore.png" `
    -Flags @(@(225, 611, 55, 38)) `
    -ExtraDraw {
        param($g)
        $bg = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(18, 32, 47))
        $g.FillRectangle($bg, 286, 610, 195, 45)
        $font = [System.Drawing.Font]::new("Arial", 31, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
        $brush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(210, 222, 236))
        $g.DrawString("Singapore", $font, $brush, 288, 610)
        $bg.Dispose()
        $font.Dispose()
        $brush.Dispose()
    }

Edit-Image `
    -InputPath "C:\Users\1212\AppData\Local\Temp\codex-clipboard-fd365f94-234b-4bdd-8df1-51b50f6a6681.jpg" `
    -OutputPath "$outDir\image2-byteforge-singapore.jpg" `
    -Flags @(
        @(176, 147, 24, 17),
        @(1352, 225, 30, 20),
        @(1521, 259, 28, 19),
        @(1647, 310, 27, 18),
        @(1783, 411, 29, 20)
    )

Edit-Image `
    -InputPath "C:\Users\1212\AppData\Local\Temp\codex-clipboard-980da7c1-410a-4019-82a7-4106fa7e1390.jpg" `
    -OutputPath "$outDir\image3-byteforge-singapore.jpg" `
    -Flags @(@(179, 390, 37, 22))

Write-Output "Saved edited images to $outDir"
