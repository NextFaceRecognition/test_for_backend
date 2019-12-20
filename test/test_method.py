import os
import time

from test.api import Agent
from test.data_helper import parse_image_name
from test.print_helper import PrintFunctions as PF
from test.config import ALLOWED_FILE_TYPE


def _allow_file_type(filename):
    filename, ext = os.path.splitext(filename)
    ext = ext.strip('.')
    return ext in ALLOWED_FILE_TYPE


def test_add_face_method(image_dir):
    """Test for add face service."""
    agent = Agent()
    print('Begin to test add face...')
    for image_name in os.listdir(image_dir):
        if not _allow_file_type(image_name):
            continue
        
        uid, name = parse_image_name(image_name)
        start_time = time.time()
        response = agent.add_face(uid, name, 
            os.path.join(image_dir, image_name))
        end_time = time.time()
        take_time = round(end_time - start_time, 3)
        
        # Parse response
        if response['code'] == 0:
            PF.print_success('Login successfully!', end='')
            print(' uid = {}, name={}, take time={}'
                  .format(uid, name, take_time))
        else:
            PF.print_warning('Login failed!')
    
    
def test_check_person_method(image_dir, mode):
    """Test for check person service."""
    agent = Agent()
    try:
        report = _run_check_test(agent, image_dir, mode)
    except KeyboardInterrupt:
        pass
    _show_test_report(report)
        

def _run_check_test(agent, image_dir, mode):
    """Define single epoch runing process."""
    report = {
        'correct': 0,
        'wrong': 0,
        'not_logined': 0,
        'not_found': 0,
        'request_err': 0,
        'server_err': 0
    }
    time_span = 0
    
    for image_name in os.listdir(image_dir):
        if not _allow_file_type(image_name):
            continue
        uid, name = parse_image_name(image_name)
        
        start_time = time.time()
        response = agent.check_person(uid, name, 
            os.path.join(image_dir, image_name),
            mode=mode)
        end_time = time.time()
        time_span += end_time - start_time
        
        parse_result = _parse_response(response, uid, name)
        report[parse_result] += 1
        
    report['total_request'] = sum(report.values())
    report['time_span'] = time_span
    
    return report
    
    
def _parse_response(response, uid, name):
    """This is a helper function to analyse response.
    Args:
        response: response from server.
        uid: user id checked.
        name: user name checked.
    """
    parse_result = None
    code = response['code']
    # When verified successfully.
    if code == 0:
        # When passed verification.
        if response['simResult'] == '1':
            # Manual check.
            if uid == response['uid']:
                PF.print_success('Correct!', end=' ')
                parse_result = 'correct'
            else:
                PF.print_warning('Wrong!', end=' ')
                parse_result = 'wrong'
            PF.print_ok_blue('Verification passed.', end=' ')
        # Verification failed.
        else:
            if uid != response['uid']:
                PF.print_success('Correct!', end=' ')
                parse_result = 'correct'
            else:
                PF.print_warning('Wrong!', end=' ')
                parse_result = 'wrong'
            PF.print_ok_blue('Verification failed.', end=' ')
        # Check information.
        print('sent: uid={}; response: uid={}, similarity={}'
                .format(uid, response['uid'], response['sim']))
        
    # When face haven't be be logined.
    elif code == 401:
        PF.print_ok_blue("Face haven't logined!", end=' ')
        print("uid:{}, name:{}".format(uid, name))
        parse_result = 'not_logined'
        
    # When face not found from image.
    elif code == 410:
        PF.print_warning("Face not found!", end=' ')
        print("uid:{}, name:{}".format(uid, name))
        parse_result = 'not_found'
    
    # When mode is not in ['1vn', '1v1'].
    elif code == 405:
        PF.print_error("Mode not allowed!")
        parse_result = 'request_err'
    
    # Unknown error.
    else:
        PF.print_error('Error occur!', end='')
        print(response)
        parse_result = 'server_err'
    
    return parse_result
            

def _show_test_report(report):
    """This functino is to show a report of the whole test process."""
    report_items = {}
    report_items['判断正确'] = report['correct']
    report_items['判断错误'] = report['wrong']
    report_items['未注册的人脸个数'] = report['not_logined']
    report_items['定位失败的人脸个数'] = report['not_found']
    report_items['请求格式错误'] = report['request_err']
    report_items['系统未知错误'] = report['server_err']
    
    report_items['准确率'] = report['correct'] / report['total_request']
    report_items['系统失效率'] = report['server_err'] / report['total_request']
    
    report_items['总时间'] = report['time_span']
    report_items['平均单个请求时间'] = report['time_span']/ report['total_request']
    
    print()
    print('{}{}{}'.format('=' * 20, 'report', '=' * 20))
    for key, value in report_items.items():
        print('{}: {}'.format(key, round(value, 3)))
    
    print('=' * 46)
    
    