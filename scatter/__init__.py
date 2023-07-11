from. import backdrop_gen,backdrop_del

modules=[
    backdrop_gen,
    backdrop_del
    ]

def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()