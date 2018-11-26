from pyldapi import Renderer, View
from flask import Response, render_template, url_for
from rdflib import Graph


class Concept:
    def __init__(
            self,
            vocab,
            uri,
            prefLabel,
            definition,
            altLabels,
            hiddenLabels,
            source,
            contributor,
            broaders,
            narrowers,
            semantic_properties
    ):
        self.vocab = vocab
        self.uri = uri
        self.prefLabel = prefLabel
        self.definition = definition
        self.altLabels = altLabels
        self.hiddenLabels = hiddenLabels
        self.source = source
        self.contributor = contributor
        self.broaders = broaders
        self.narrowers = narrowers
        self.semantic_properties = semantic_properties


class ConceptRenderer(Renderer):
    def __init__(self, request, concept):
        self.request = request
        self.views = self._add_skos_view()
        self.navs = []  # TODO: add in other nav items for Concept

        self.concept = concept

        super().__init__(
            self.request,
            self.concept.uri,
            self.views,
            'skos'
        )

    def _add_skos_view(self):
        return {
            'skos': View(
                'Simple Knowledge Organization System (SKOS)',
                'SKOS is a W3C recommendation designed for representation of thesauri, classification schemes, '
                'taxonomies, subject-heading systems, or any other type of structured controlled vocabulary.',
                ['text/html', 'application/json'] + self.RDF_MIMETYPES,
                'text/html',
                languages=['en'],  # default 'en' only for now
                namespace='http://www.w3.org/2004/02/skos/core#'
            )
        }

    def render(self):
        if self.view == 'alternates':
            return self._render_alternates_view()
        elif self.view == 'skos':
            if self.format in Renderer.RDF_MIMETYPES:
                return self._render_skos_rdf()
            else:
                return self._render_skos_html()

    def _render_skos_rdf(self):
        # get Concept RDF
        import model.source_rva as rva
        v = rva.RVA().get_resource_rdf(self.vocab_id, self.uri)
        g = Graph().load(v, format='turtle')

        # serialise in the appropriate RDF format
        if self.format in ['application/rdf+json', 'application/json']:
            return g.serialize(format='json-ld')
        else:
            return g.serialize(format=self.format)

    def _render_skos_html(self):
        _template_context = {
            'uri': self.uri,
            'concept': self.concept,
            'navs': self.navs
        }

        return Response(
            render_template(
                'concept.html',
                **_template_context
            ),
            headers=self.headers
        )

    def _render_alternates_view(self):
        super().__init__(
            self.request,
            url_for('routes.object') + '?vocab_uri=' + self.concept.vocab.id,
            self.views,
            self.default_view_token
        )
