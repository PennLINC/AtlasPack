docker run -it \
    -v /Users/taylor/Documents/tsalo/AtlasPack:/AtlasPack \
    -v /Users/taylor/.cache/templateflow:/templateflow \
    --env TEMPLATEFLOW_HOME=/templateflow \
    --entrypoint /bin/bash \
    pennlinc/xcp_d:0.1.3
