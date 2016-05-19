var React = require("react");
var actions = require("../actions/LoginActions");


module.exports = React.createClass({
    getInitialState:function(){
      return {
          email:"",
          password:"",
          loginSuccessCallback:this.props.loginSuccessCallback
      }  
    },
    submitLoginCredentials:function(e){
        e.preventDefault();
        actions.submitLoginCredentials(this.state);
    },
    handleInputChange:function(e){
      e.preventDefault();
      var name = e.target.name;
      var state = this.state;
      state[name] = e.target.value;
      this.setState(state);
    },
    render:function(){
        return(
            <div id="login-form">
                <h3>Login</h3>
                <fieldset>
                    <form className="form" onSubmit={this.submitLoginCredentials}>
                        <div className="form-group">
                            <label className="control-label" htmlFor="email">email:</label>
                            <input type="text" className="form-control" id="email" name="email" value={this.state.email} onChange={this.handleInputChange} placeholder="joe@schmoe.com" />                    
                        </div>
                        <div className="form-group">
                            <label className="control-label" htmlFor="password">password:</label>
                            <input type="text" className="form-control" id="password" name="password" value={this.state.password} onChange={this.handleInputChange} placeholder="password" />                    
                        </div>
                        <div className="form-group">
                            <button className="btn" type="submit">Login</button>
                        </div>
                        <footer class="clearfix">
                          <p><span className="info">?</span><a href="#">Forgot Password</a></p>
                        </footer>
                    </form>
                </fieldset>
            </div>
        )
    }
})

  