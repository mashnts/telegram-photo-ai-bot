from user_agents import parse


def get_device_type(user_agent_string):
    user_agent = parse(user_agent_string)

    if user_agent.is_mobile:
        return 'mobile'
    elif user_agent.is_tablet:
        return 'tablet'
    elif user_agent.is_pc:
        return 'desktop'
    else:
        return 'other'


def get_browser_info(user_agent_string):
    user_agent = parse(user_agent_string)
    return user_agent.browser.family


def get_os_info(user_agent_string):
    user_agent = parse(user_agent_string)
    return user_agent.os.family


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
