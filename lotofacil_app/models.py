

from django.db import models


class Base(models.Model):
    created = models.DateTimeField('Data de criação', auto_now_add=True)
    updated = models.DateTimeField('Última atualização', auto_now=True)
    availability = models.BooleanField('Disponibilidade', default=True)

    # Configurar para ser usado por qualquer outro modelo
    class Meta:
        abstract = True


class Game(Base):
    code = models.CharField('Código do jogo', max_length=100)

    def __str__(self):
        return self.code

    # Rótulos para o Django template admin
    class Meta:
        verbose_name = 'Jogo'
        verbose_name_plural = verbose_name + 's'


class NewGame(Base):
    game_text = models.CharField('', max_length=100)

    def __str__(self):
        return self.game_text

    # Rótulos para o Django template admin
    class Meta:
        verbose_name = 'Novo jogo'
        verbose_name_plural = verbose_name + 's'
