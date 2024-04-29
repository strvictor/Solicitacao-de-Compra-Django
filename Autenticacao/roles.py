from rolepermissions.roles import AbstractUserRole


class CoordenadoresPermissoes(AbstractUserRole):
    available_permissions = {
                                'aprovar_pedidos': True,
                                'reprovar_pedidos': True,
                                'visualizar_pedidos': True
                             }
    
class DiretorPermissoes(AbstractUserRole):
    available_permissions = {
                                'aprovar_pedidos': True,
                                'reprovar_pedidos': True,
                                'visualizar_pedidos': True,
                                'visualizar_relatorios': True
                             }