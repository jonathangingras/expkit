

class ChainedAttributeError(AttributeError):
    pass


def get_chained_attribute(initial_object, attributes_chain):
    prev_result = None
    result = initial_object

    for element in attributes_chain:
        prev_result = result
        try:
            result = getattr(result, element)
        except AttributeError:
            try:
                result = result[element]
            except KeyError:
                raise ChainedAttributeError("invalid chain \"{}\" for object \"{}\"".format(attributes_chain, initial_object))

    return result, prev_result


class SelfCalledForwarder(object):
    def __init__(self, caller_chain, callee_chain):
        self.caller_chain = caller_chain
        self.callee_chain = callee_chain


    def __call__(self, chainable):
        arg = get_chained_attribute(chainable, self.callee_chain)[0]
        method, caller = get_chained_attribute(chainable, self.caller_chain)
        return method(caller, arg)
