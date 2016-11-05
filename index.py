"""
This is a simple Alexa Skill that reads the top headlines from BBC News.
"""
from __future__ import print_function
import requests
import json


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetNewsIntent":
        print('GetNewsIntent')
        return get_news(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return get_cancel_response(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    session_attributes = {}
    card_title = "News Headlines"
    speech_output = "Hello, I can read you the top news headlines. " \
                    "For example, you can say, " \
                    "what's in the news.  " \

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what news you want. " \
                    "For example, you can say, " \
                    "what's in the news.  " \

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = "Help"
    speech_output = "Need Help? I can read you the top news headlines. Just say, " \
                    "what's in the news." 
    reprompt_text = "I'm sorry, I didn't hear what you said. " \
                    "Please tell me if you want news."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_cancel_response(intent, session):
    session_attributes = {}
    card_title = "Goodbye"
    speech_output = "Have a good day, Chris!"
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_url():
    """
    Returns the URL for the RSS feed based on the news section
    """
    return 'http://api.nytimes.com/svc/topstories/v1/home.json?api-key=4f085be2b93a4c4b8ca57c3d59aa1942'


def get_news(intent, session, num_headlines=3):
    """ Gets the news headlines"""
    card_title = "News Headlines"
    session_attributes = session.get('attributes', {})

    url = get_url()
    r = requests.get(url)
    parsed = json.loads(r.content)
    headlines = []
    for i in range(len(parsed['results'])):
        headlines.append(parsed['results'][i]['title'])

    speech_output = "Here's what's new in " + headlines[0]
    #for headline in headlines:
    #   speech_output += " " + headline

    reprompt_text = None
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
