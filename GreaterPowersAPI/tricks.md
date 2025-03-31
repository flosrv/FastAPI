

netstat -ano | findstr :8000 | foreach { taskkill /PID $_.Split()[-1] /F }
