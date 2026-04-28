import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

class EmailBackend(SMTPEmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            
            if self.use_tls:
                context = ssl.create_default_context()
                if getattr(self, 'ssl_keyfile', None) and getattr(self, 'ssl_certfile', None):
                    context.load_cert_chain(certfile=self.ssl_certfile, keyfile=self.ssl_keyfile)
                self.connection.starttls(context=context)
                
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
            return False
