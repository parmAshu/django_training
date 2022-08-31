from django.db import models

# Create your models here.
class DriveFile( models.Model ):
    fl = models.FileField( upload_to='files' )
    fileName = models.CharField( max_length=100 )

    def __str__( self ):
        return self.fl.name