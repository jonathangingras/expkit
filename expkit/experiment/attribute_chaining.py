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


class ChainedAttributeCallForwarder(object):
    def __init__(self, function_chain, *arguments_chains):
        self.function_chain = function_chain
        self.arguments_chains = arguments_chains


    def __eq__(self, other):
        return isinstance(other, ChainedAttributeCallForwarder) and \
            self.function_chain == other.function_chain and \
            self.arguments_chains == other.arguments_chains


    def __call__(self, chainable):
        def recurse(chain):
            try:
                return call_if_callable(get_chained_attribute(chainable, chain))
            except TypeError:
                return call_if_callable(chain)

        function = get_chained_attribute(chainable, self.function_chain)

        return function(*tuple(map(recurse, self.arguments_chains)))
