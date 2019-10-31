# coding=utf-8

from multivac.src.gan.gen_pyt.asdl.lang.eng.eng_asdl_helper \
    import asdl_ast_to_english, english_ast_to_asdl_ast
from multivac.src.rdf_graph.rdf_parse import tokenize_text
from multivac.src.gan.gen_pyt.asdl.transition_system \
    import TransitionSystem, GenTokenAction

from multivac.src.gan.gen_pyt.common.registerable import Registrable


@Registrable.register('english')
class EnglishTransitionSystem(TransitionSystem):
    self.parser = StanfordParser(annots = "tokenize ssplit parse")

    def tokenize_text(self, text, mode=None):
        return tokenize_text(text, mode)

    def surface_text_to_ast(self, text):
        p = self.parser.get_parse(text)['parse']
        return english_ast_to_asdl_ast(p)

    def ast_to_surface_text(self, asdl_ast):
        text = asdl_ast_to_english(asdl_ast)
        return text

    def compare_ast(self, hyp_ast, ref_ast):
        hyp_text = self.ast_to_surface_text(hyp_ast)
        ref_reformatted_text = self.ast_to_surface_text(ref_ast)

        ref_text_tokens = tokenize_text(ref_reformatted_text)
        hyp_text_tokens = tokenize_text(hyp_text)

        return ref_text_tokens == hyp_text_tokens

    def get_primitive_field_actions(self, realized_field):
        actions = []

        if realized_field.value is not None:
            field_values = [realized_field.value]

            tokens = []

            for field_val in field_values:
                tokens.extend(field_val.split(' ') + ['</primitive>'])

            for tok in tokens:
                actions.append(GenTokenAction(tok))

        return actions

    def is_valid_hypothesis(self, hyp, **kwargs):
        try:
            hyp_text = self.ast_to_surface_text(hyp.tree)
            new_tree = self.surface_text_to_ast(hyp_text)
            assert hyp.tree == new_tree
        except:
            return False
        return True
