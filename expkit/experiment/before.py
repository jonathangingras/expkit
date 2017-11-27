from ..utils.arguments import call_if_callable


class ChainedAttributeError(AttributeError):
    pass


def get_chained_attribute(initial_object, attributes_chain):
    result = initial_object

    for element in attributes_chain:
        try:
            result = getattr(result, element)
        except AttributeError:
            try:
                result = result[element]
            except (TypeError, KeyError) as error:
                raise ChainedAttributeError(
                    "invalid chain \"{}\" for object \"{}\"".format(
                        attributes_chain, initial_object), error)

    return result


class SingleObjectForwarder(object):
    def __init__(self, caller_chain, arg_chain):
        self.caller_chain = caller_chain
        self.arg_chain = arg_chain


    def __call__(self, chainable):
        arg = call_if_callable(get_chained_attribute(chainable, self.arg_chain))
        method = get_chained_attribute(chainable, self.caller_chain)
        return method(arg)
