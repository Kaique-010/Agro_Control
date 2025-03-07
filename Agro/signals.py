from django.db.models.signals import post_save, pre_delete, pre_save
from services.notify import Notify
from django.dispatch import receiver
from django.forms import ValidationError
from .models import Animal, MovimentacaoEstoque, EstoqueFazenda, EventoAnimal

# Atualiza o estoque após salvar uma movimentação
@receiver(post_save, sender=MovimentacaoEstoque)
def atualizar_estoque(sender, instance, created, **kwargs):
    if created:  # Apenas para novas movimentações
        estoque, _ = EstoqueFazenda.objects.get_or_create(
            fazenda=instance.fazenda,
            produto=instance.produto,
            empresa=instance.empresa,
            filial=instance.filial
        )
        
        if instance.tipo == 'entrada':
            novo_total = estoque.quantidade + instance.quantidade
            if instance.custo_unitario:
                # Cálculo do custo médio ponderado
                estoque.custo_medio_atualizado = (
                    (estoque.custo_medio_atualizado * estoque.quantidade) +
                    (instance.custo_unitario * instance.quantidade)
                ) / novo_total
        else:  # Saída
            novo_total = estoque.quantidade - instance.quantidade
            # O custo médio não muda na saída

        estoque.quantidade = max(novo_total, 0)  # Garante que não fique negativo
        estoque.save()

@receiver(pre_delete, sender=MovimentacaoEstoque)
def reverter_estoque(sender, instance, **kwargs):
    try:
        estoque = EstoqueFazenda.objects.get(fazenda=instance.fazenda, produto=instance.produto, empresa=instance.empresa, filial=instance.filial)
        if instance.tipo == 'entrada':
            estoque.quantidade = max(estoque.quantidade - instance.quantidade, 0)
        else:
            estoque.quantidade += instance.quantidade
        estoque.save()
    except EstoqueFazenda.DoesNotExist:
        pass

# Criação automática de eventos ao salvar um animal
@receiver(post_save, sender=Animal)
def criar_evento_nascimento(sender, instance, created, **kwargs):
    if created:
        EventoAnimal.objects.create(
            animal=instance,
            tipo_evento='nascimento',
            data_evento=instance.data_nascimento or instance.created_at,
            descricao=f"Nascimento do animal {instance.identificacao}"
        )


@receiver(pre_save, sender=MovimentacaoEstoque)
def validar_saida_estoque(sender, instance, **kwargs):
    """ Valida se há estoque suficiente antes de registrar a saída """
    if instance.tipo == 'saida':
        estoque = EstoqueFazenda.objects.filter(fazenda=instance.fazenda, produto=instance.produto, empresa=instance.empresa, filial=instance.filial).first()
        if not estoque or instance.quantidade > estoque.quantidade:
            raise ValidationError("Não há estoque suficiente para esta saída.")


@receiver(pre_save, sender=MovimentacaoEstoque)
def send_webhook(sender, instance, **kwargs):
    if instance.tipo ==  'saida':
        notify = Notify()
        data = {
            'produto': str(instance.produto),
            'quantidade' :str(instance.quantidade),
            'data': str(instance.data)
        }
        notify.send_event(data)
        
        print('Enviar para o Webhook a Saída')