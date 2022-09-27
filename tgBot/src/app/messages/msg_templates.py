class Templates:
    def error_reply(self, header: str, msg: str) -> str:
        return f"""<p>🚨 {header} 🚨</p>
                        <br>
                        {msg}    
                        <br>
                        <hl>   
       """
