# Grab a visible browser window (logged-in pages Claude drives via Claude in Chrome) to PNG.
# Usage: powershell -File grab_window.ps1 -Title "Google ไดรฟ์" -Out C:\...\shots\20-drive.png [-Top 0]
# -Top trims pixels from the top (tab strip + address bar) so only the page shows.
param([string]$Title, [string]$Out, [int]$Top = 0)
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System; using System.Text; using System.Runtime.InteropServices; using System.Collections.Generic;
public class Win {
  public delegate bool EP(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EP f, IntPtr l);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("dwmapi.dll")] public static extern int DwmGetWindowAttribute(IntPtr h, int a, out R r, int s);
  public struct R { public int L, T, Rt, B; }
  public static List<KeyValuePair<IntPtr,string>> All() {
    var l = new List<KeyValuePair<IntPtr,string>>();
    EnumWindows((h, p) => { if (IsWindowVisible(h)) { var s = new StringBuilder(512); GetWindowText(h, s, 512);
      if (s.Length > 0) l.Add(new KeyValuePair<IntPtr,string>(h, s.ToString())); } return true; }, IntPtr.Zero);
    return l; }
}
'@
[Win]::SetProcessDPIAware() | Out-Null
$w = [Win]::All() | Where-Object { $_.Value -like "*$Title*" -and $_.Value -like '*Chrome*' } | Select-Object -First 1
if (-not $w) { "window not found: $Title"; [Win]::All() | ForEach-Object { $_.Value }; exit 1 }
[Win]::ShowWindow($w.Key, 9) | Out-Null; [Win]::SetForegroundWindow($w.Key) | Out-Null; Start-Sleep -Milliseconds 700
$r = New-Object Win+R; [Win]::DwmGetWindowAttribute($w.Key, 9, [ref]$r, 16) | Out-Null
$wd = $r.Rt - $r.L; $ht = $r.B - $r.T - $Top
$bmp = New-Object Drawing.Bitmap $wd, $ht; $g = [Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($r.L, $r.T + $Top, 0, 0, $bmp.Size); $bmp.Save($Out, [Drawing.Imaging.ImageFormat]::Png)
"$($w.Value) -> $Out ($wd x $ht)"
