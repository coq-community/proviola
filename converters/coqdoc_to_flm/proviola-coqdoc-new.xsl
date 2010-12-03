<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"  
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
    <head>
      <link href="coqdoc.css" type="text/css" rel="stylesheet" />
      <link href="proviola.css" type="text/css" rel="stylesheet" />
      
      <script type = "text/javascript">
        var responses = new Array();

        function mouseover(id, scene) {
          set_response(get_response(id), scene);
        };

        function mouseout(scene) {
          set_response("", scene);
        };

        function set_array() {
          <xsl:for-each select="movie/film/frame">
            <xsl:variable name="data">
              <xsl:call-template name="replace">
                <xsl:with-param name="string">
                  <xsl:value-of 
                    select="translate(response, '&#x0A;', '&#x09;') "/> 
                </xsl:with-param>
                <xsl:with-param name="from">&quot;</xsl:with-param>
                <xsl:with-param name="to">\"</xsl:with-param>
              </xsl:call-template>
            </xsl:variable>

            i = <xsl:value-of select="@frameNumber"/>;
            data = "<xsl:value-of select="$data"/>";
            responses[i]=data;
          </xsl:for-each>
        };
        
        function get_response(id) {
          return responses[id];
        };

        function set_response(response, scene) {
          goalId = "goal"+scene;
          elById = document.getElementById(goalId);
          if(elById){ 
            goalSpan = elById.getElementsByTagName("span")[0];
            goalSpan.innerHTML = response.replace(/&#x09;/g , '\n');
          }
        };
      </script>
    </head>

    <body onload="set_array()">
      <xsl:for-each select="movie/scenes">
        <xsl:apply-templates />
      </xsl:for-each>
    </body>
  </html>
</xsl:template>

<xsl:template match="frame">
  <xsl:param name="sceneRef"/>
  <xsl:param name="scene-type"/>
 
  <xsl:choose>
  <xsl:when test="$scene-type = 'doc'">
    <xsl:copy-of select = "command-coqdoc/node()"/>
  </xsl:when>
  <xsl:otherwise>
    <span class="command">
      <xsl:attribute name="onmouseout">
      mouseout('<xsl:value-of select="$sceneRef"/>');
      </xsl:attribute>
      <xsl:attribute name="onmouseover">
      mouseover(<xsl:value-of select="@frameNumber"/>, '<xsl:value-of select="$sceneRef"/>');
      </xsl:attribute>

      <xsl:copy-of select = "command-coqdoc/node()"/>
    </span>
  </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="frame-reference">
  <xsl:param name="sceneRef">-1</xsl:param>
  <xsl:param name="scene-type">doc</xsl:param>
  <xsl:variable name = "ref">
    <xsl:value-of select="@frameNumber" />
  </xsl:variable>
  <xsl:apply-templates select="/movie/film/frame[@frameNumber = $ref]">
    <xsl:with-param name="sceneRef" select="$sceneRef"/>
    <xsl:with-param name="scene-type" select="$scene-type"/>
  </xsl:apply-templates>
</xsl:template>

<xsl:template match="scene">
  <xsl:param name="sceneRef">-1</xsl:param>
  <xsl:param name="scene-type">doc</xsl:param>
  <xsl:if test="not(@class='hidden')">

  <div>
    <xsl:for-each select="@*">
      <xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
    </xsl:for-each>

    <xsl:apply-templates>
      <xsl:with-param name="sceneRef">
        <xsl:choose>
        <xsl:when test="$sceneRef &lt; 0">
          <xsl:value-of select="@sceneNumber" />
        </xsl:when>

        <xsl:otherwise>
          <xsl:value-of select="$sceneRef"/>_<xsl:value-of select="@sceneNumber" />
        </xsl:otherwise> 
        </xsl:choose>
       </xsl:with-param>
       <xsl:with-param name="scene-type">
        <xsl:value-of select="@class"/>
       </xsl:with-param>
     </xsl:apply-templates>
  </div> 

  <xsl:if test="@class='code'">
    <xsl:variable name="goalId">
      <xsl:choose>
        <xsl:when test="$sceneRef &lt; 0">
          <xsl:value-of select="@sceneNumber" />
        </xsl:when>
    
        <xsl:otherwise>
          <xsl:value-of select="$sceneRef"/>_<xsl:value-of select="@sceneNumber" />
        </xsl:otherwise>

      </xsl:choose>
    </xsl:variable>

    <div class="goal">
      <xsl:attribute name="id">
        <xsl:text>goal</xsl:text><xsl:value-of select="$goalId"/>
      </xsl:attribute>
      <pre> 
        <span>
        </span>
      </pre>
    </div>
  </xsl:if>

  </xsl:if>
</xsl:template>

<xsl:template name="replace">
  <xsl:param name="string"/>
  <xsl:param name="from"/>
  <xsl:param name="to"/>
  <xsl:choose>
    <xsl:when test= "contains($string, $from)">
      <xsl:value-of select="substring-before($string, $from)"/>
      <xsl:value-of select="$to"/>
      <xsl:call-template name="replace">
        <xsl:with-param name="string" 
                        select="substring-after($string, $from)"/>
        <xsl:with-param name="from" select="$from"/>
        <xsl:with-param name="to" select="$to"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$string"/> 
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>
            

</xsl:stylesheet>
