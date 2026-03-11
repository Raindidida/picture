"""
从Chrome复制Cookies数据库（处理文件锁定）
"""
import sqlite3
import shutil
import os
import json
import base64
import tempfile
import ctypes
import sys

def copy_locked_file(src, dst):
    """使用Volume Shadow Copy服务复制锁定的文件"""
    try:
        # 方法1: 使用robocopy
        result = os.popen(f'robocopy /B "{os.path.dirname(src)}" "{os.path.dirname(dst)}" "{os.path.basename(src)}" /R:0 /W:0').read()
        if os.path.exists(dst):
            return True
    except:
        pass
    
    try:
        # 方法2: 使用esentutl
        result = os.popen(f'esentutl /y "{src}" /d "{dst}" /o').read()
        if os.path.exists(dst):
            return True
    except:
        pass
    
    return False

def get_douyin_cookies():
    output_file = r"E:\漫剧\douyin_cookies.txt"
    
    # 安装依赖
    os.system("pip install cryptography pywin32 -q 2>nul")
    
    import win32crypt
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    
    # Chrome配置
    browsers = {
        'chrome': {
            'state': os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State'),
            'cookies': os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Network', 'Cookies'),
        },
        'edge': {
            'state': os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Local State'),
            'cookies': os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Network', 'Cookies'),
        }
    }
    
    for browser_name, paths in browsers.items():
        print(f"尝试 {browser_name}...")
        
        if not os.path.exists(paths['cookies']):
            print(f"  找不到cookies文件")
            continue
        
        # 读取AES密钥
        try:
            with open(paths['state'], 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
            aes_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            print(f"  AES密钥获取成功，长度: {len(aes_key)}")
        except Exception as e:
            print(f"  密钥读取失败: {e}")
            continue
        
        # 复制数据库文件
        tmp_dir = tempfile.mkdtemp()
        tmp_db = os.path.join(tmp_dir, 'Cookies')
        
        copied = False
        # 方法1: 普通复制
        try:
            shutil.copy2(paths['cookies'], tmp_db)
            copied = True
            print("  普通复制成功")
        except Exception as e:
            print(f"  普通复制失败: {e}")
        
        # 方法2: robocopy
        if not copied:
            src_dir = os.path.dirname(paths['cookies'])
            src_name = os.path.basename(paths['cookies'])
            os.system(f'robocopy /B "{src_dir}" "{tmp_dir}" "{src_name}" /R:0 /W:0 >nul 2>&1')
            if os.path.exists(tmp_db):
                copied = True
                print("  robocopy复制成功")
        
        # 方法3: esentutl
        if not copied:
            os.system(f'esentutl /y "{paths["cookies"]}" /d "{tmp_db}" /o >nul 2>&1')
            if os.path.exists(tmp_db):
                copied = True
                print("  esentutl复制成功")
        
        if not copied:
            print("  所有复制方法均失败，跳过")
            continue
        
        # 读取并解密cookies
        cookies = []
        try:
            conn = sqlite3.connect(f'file:{tmp_db}?mode=ro', uri=True)
            cursor = conn.cursor()
            
            # 查询抖音相关cookies
            cursor.execute("""
                SELECT host_key, name, encrypted_value, path, 
                       CASE WHEN expires_utc > 0 THEN (expires_utc - 11644473600000000) / 1000000 ELSE 0 END,
                       is_secure, is_httponly 
                FROM cookies 
                WHERE host_key LIKE '%douyin%' 
                   OR host_key LIKE '%.snssdk.com%'
                   OR host_key LIKE '%.toutiao.com%'
            """)
            
            rows = cursor.fetchall()
            print(f"  找到 {len(rows)} 个抖音相关cookies")
            
            for row in rows:
                host, name, enc_val, path, expires, secure, httponly = row
                value = ""
                
                if enc_val:
                    try:
                        prefix = enc_val[:3]
                        if prefix in [b'v10', b'v11', b'v20']:
                            nonce = enc_val[3:15]
                            ciphertext = enc_val[15:-16]
                            tag = enc_val[-16:]
                            cipher = Cipher(
                                algorithms.AES(aes_key),
                                modes.GCM(nonce, tag),
                                backend=default_backend()
                            )
                            decryptor = cipher.decryptor()
                            value = (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8', errors='replace')
                        else:
                            value = win32crypt.CryptUnprotectData(enc_val, None, None, None, 0)[1].decode('utf-8', errors='replace')
                    except Exception as e:
                        pass
                
                if value:
                    cookies.append({
                        'domain': host,
                        'name': name,
                        'value': value,
                        'path': path,
                        'expires': int(expires) if expires else 0,
                        'secure': bool(secure),
                        'httponly': bool(httponly)
                    })
            
            conn.close()
            
        except Exception as e:
            print(f"  读取数据库失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except:
                pass
        
        if cookies:
            # 写入Netscape格式
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# Netscape HTTP Cookie File\n")
                f.write("# Generated by extract_cookies.py\n\n")
                for c in cookies:
                    domain = c['domain']
                    subdomain = "TRUE" if domain.startswith('.') else "FALSE"
                    secure = "TRUE" if c['secure'] else "FALSE"
                    f.write(f"{domain}\t{subdomain}\t{c['path']}\t{secure}\t{c['expires']}\t{c['name']}\t{c['value']}\n")
            
            print(f"\n成功! 导出 {len(cookies)} 个cookies")
            print(f"文件: {output_file}")
            return True
        else:
            print(f"  未能解密到有效cookies")
    
    return False

if __name__ == "__main__":
    success = get_douyin_cookies()
    if not success:
        print("\n自动提取失败，请手动操作：")
        print("1. 打开Chrome，访问 https://www.douyin.com 并登录")
        print("2. 安装扩展 'Get cookies.txt LOCALLY'")
        print("   (https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)")
        print("3. 点击扩展图标 -> 选择 douyin.com -> Export as Netscape")
        print("4. 保存文件到: E:\\漫剧\\douyin_cookies.txt")
        sys.exit(1)
