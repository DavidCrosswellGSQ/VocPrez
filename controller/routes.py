from flask import Blueprint, Response, request, render_template, url_for
import model
from model.vocabulary import VocabularyRenderer
from model.concept import ConceptRenderer
from model.collection import CollectionRenderer
from model.skos_register import SkosRegisterRenderer
import _config as config
import markdown
from flask import Markup

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return render_template(
        'index.html',
        title='SKOS Styler',
        navs={}
    )


@routes.route('/vocabulary/')
def vocabularies():
    vocabs = model.rva().list_vocabularies()

    return SkosRegisterRenderer(
        request,
        [],
        vocabs,
        'Vocabularies',
        len(vocabs)
    ).render()


@routes.route('/vocabulary/<vocab_id>')
def vocabulary(vocab_id):
    # decide what source to use based on ID prefix, get vocab from appropriate source
    if vocab_id.startswith('rva-'):
        vocab = model.rva().get_vocabulary(vocab_id)
    else:
        # no other sorts for now
        pass

    return VocabularyRenderer(
        request,
        vocab
    ).render()


@routes.route('/collection/')
def collections():
    return render_template(
        'register.html',
        title='Collections',
        register_class='Collections',
        navs={}
    )


@routes.route('/concept/')
def concepts():
    return render_template(
        'register.html',
        title='Concepts', register_class='Concepts',
        navs={}
    )


@routes.route('/object')
def object():
    """
    This is the general RESTful endpoint and corresponding Python function to handle requests for individual objects,
    be they a Vocabulary, Concept Scheme, Collection or Concept. Only those 4 classes of object are supported for the
    moment.

    An HTTP URI query string argument parameter 'vocab_id' must be supplied, indicating the vocab this object is within
    An HTTP URI query string argument parameter 'uri' must be supplied, indicating the URI of the object being requested

    :return: A Flask Response object
    :rtype: :class:`flask.Response`
    """
    if request.values.get('vocab_id') is None and request.values.get('uri'):
        return Response(
            'Query String Arguments \'vocab_id\' & \'uri\' must be supplied for this endpoint'
        )
    elif request.values.get('vocab_id') is None:
        return Response(
            'A Query String Argument \'vocab_id\' must be supplied for this endpoint, '
            'indicating the vocab this object is within'
        )
    elif request.values.get('uri') is None:
        return Response(
            'A Query String Argument \'uri\' must be supplied for this endpoint, '
            'indicating an object within a vocabulary'
        )

    vocab_id = request.values.get('vocab_id')
    vocab = model.rva().get_vocabulary(vocab_id)
    uri = request.values.get('uri')
    import model.source_rva as RVA
    c = RVA.RVA().get_object_class(vocab_id, uri)

    if c == 'http://www.w3.org/2004/02/skos/core#Concept':
        concept = model.rva().get_concept(vocab, uri)

        return ConceptRenderer(
            request,
            concept
        ).render()
    elif c == 'http://www.w3.org/2004/02/skos/core#Collection':
        collection = model.rva().get_collection(vocab, uri)

        return CollectionRenderer(
            request,
            collection
        ).render()
    # conflate Vocab with ConceptScheme
    elif c == 'http://www.w3.org/2004/02/skos/core#ConceptScheme' or c == 'http://purl.org/vocommons/voaf#Vocabulary':
        # assume vocab is an RVA vocab for now
        # vocab object already found above, so just render
        return VocabularyRenderer(
            request,
            vocab
        ).render()


@routes.route('/about')
def about():
    import os

    # using basic Markdown method from http://flask.pocoo.org/snippets/19/
    with open(os.path.join(config.APP_DIR, 'README.md')) as f:
        content = f.read()

    content = Markup(markdown.markdown(content))
    return render_template(
        'about.html',
        title='About',
        navs={},
        content=content
    )
